#include "TCPServer.h"
#include "Sockets.h"
#include "SocketSubsystem.h"
#include "Networking.h"


DEFINE_LOG_CATEGORY(LogServer);


ATCPServer::ATCPServer()
{
    PrimaryActorTick.bCanEverTick = true;
}

void ATCPServer::BeginPlay()
{
    Super::BeginPlay();
    StartTCPListener();
    CameraManager = NewObject<UCameraManager>();
    ObjectManager = NewObject<UObjectManager>();

    UWorld* World = GetWorld();
    CameraManager->InitializeWorld(World);
    ObjectManager->InitializeWorld(World);


    UE_LOG(LogServer, Log, TEXT("spawning new camera"));
}

void ATCPServer::Tick(float DeltaTime)
{
    Super::Tick(DeltaTime);
    Main();
}

FString ATCPServer::ParseAndDispatch(FString& Message) {
    FString ClientMessage;
    
    TSharedPtr<FJsonObject> JsonObject;
    TSharedRef<TJsonReader<>> Reader = TJsonReaderFactory<>::Create(Message);

    if (FJsonSerializer::Deserialize(Reader, JsonObject) && JsonObject.IsValid())
    {
        FString Action;
        if (JsonObject->TryGetStringField(TEXT("action"), Action)) {
            if (Action == TEXT("add_object")) {
                ClientMessage = ObjectManager->AddObject(JsonObject);
            }
            else if (Action == TEXT("modify_object")) {
                ClientMessage = ObjectManager->ModifyObject(JsonObject);
            }
            else if (Action == TEXT("add_camera")) {
                ClientMessage = CameraManager->AddCamera(JsonObject);
            }
            else if (Action == TEXT("modify_camera")) {
                ClientMessage = CameraManager->ModifyCamera(JsonObject);
            }
            else if (Action == TEXT("get_image")) {
                ClientMessage = CameraManager->GetImage(JsonObject);
            }
            else if (Action == TEXT("add_lighting")) {
                //LightingManager->AddLighting(JsonObject);
            }
            else if (Action == TEXT("get_camera_info")) {
                UE_LOG(LogTemp, Log, TEXT("Logging camera database... %d"), CameraManager->CameraDatabase.Num());
                ClientMessage = CameraManager->GetCameraInfo(JsonObject);
            }
            else if (Action == TEXT("pick_up")) {
                CallBlueprintFunction(JsonObject);
            }
        }
    }
    return ClientMessage;
}

void ATCPServer::Main()
{
    if (!ClientSocket) {
        CheckForConnections();
    }
    else {
        if (ClientSocket->GetConnectionState() == SCS_Connected)
        {
            FString ReceivedMessage = ReceiveData();
            UE_LOG(LogServer, Log, TEXT("%s"), *ReceivedMessage);

            if (!ReceivedMessage.IsEmpty()) {
                FString result = ParseAndDispatch(ReceivedMessage);
                SendBackToClient(result);
            }
        }
        else {
            ISocketSubsystem::Get(PLATFORM_SOCKETSUBSYSTEM)->DestroySocket(ClientSocket);
            ClientSocket = nullptr;
            UE_LOG(LogServer, Log, TEXT("Client disconnected"));
        }
    }
}


bool ATCPServer::StartTCPListener()
{
    // Obtain the socket subsystem
    SocketSubsystem = ISocketSubsystem::Get(PLATFORM_SOCKETSUBSYSTEM);
    if (!SocketSubsystem)
    {
        UE_LOG(LogServer, Error, TEXT("Unable to get SocketSubsystem"));
        return false;
    }
    else {
        UE_LOG(LogServer, Log, TEXT("Got SocketSubsystem"));
    }

    // Create the TCP listener socket
    ServerSocket = SocketSubsystem->CreateSocket(NAME_Stream, TEXT("TCP Server"), false);
    if (!ServerSocket)
    {
        UE_LOG(LogServer, Error, TEXT("Unable to create TCP Socket"));
        return false;
    }
    else {
        UE_LOG(LogServer, Log, TEXT("Created TCP Socket"));
    }

    // Set up the server address
    TSharedRef<FInternetAddr> ServerAddr = SocketSubsystem->CreateInternetAddr();
    ServerAddr->SetIp(TEXT("0.0.0.0"), bindSocketSuccess);
    ServerAddr->SetPort(port);

    // Bind the socket to the address
    if (!ServerSocket->Bind(*ServerAddr))
    {
        UE_LOG(LogServer, Error, TEXT("Unable to bind socket to address"));
        return false;
    }
    else {
        UE_LOG(LogServer, Log, TEXT("Socket successfully bound to address"));
    }

    // Start listening on the socket
    if (!ServerSocket->Listen(8))
    {
        UE_LOG(LogServer, Error, TEXT("Unable to start listening on socket"));
        return false;
    }
    else {
        UE_LOG(LogServer, Log, TEXT("Server started listening on port %d"), port);
    }
    return true;
}

void ATCPServer::CheckForConnections()
{
    bool Pending;
    if (ServerSocket->HasPendingConnection(Pending) && Pending)
    {
        ClientSocket = ServerSocket->Accept(TEXT("Accepted Client Connection"));
    }
}

FString ATCPServer::ReceiveData()
{
    uint32 Size;
    while (ClientSocket->HasPendingData(Size))
    {
        TArray<uint8> ReceivedData;
        ReceivedData.SetNumUninitialized(FMath::Min(Size, 65507u));

        int32 Read = 0;
        ClientSocket->Recv(ReceivedData.GetData(), ReceivedData.Num(), Read);

        // Ensure the data is null-terminated
        ReceivedData.Add(0);

        FString ReceivedString = FString(UTF8_TO_TCHAR(reinterpret_cast<const char*>(ReceivedData.GetData())));
        UE_LOG(LogServer, Log, TEXT("Received Data: %s"), *ReceivedString);
        return ReceivedString;
    }
    return FString();
}

void ATCPServer::SendBackToClient(const FString& Message)
{
    if (ClientSocket && ClientSocket->GetConnectionState() == SCS_Connected)
    {
        FTCHARToUTF8 Convert(*Message);
        int32 BytesSent = 0;
        bool bSuccessful = ClientSocket->Send((uint8*)Convert.Get(), Convert.Length(), BytesSent);

        if (bSuccessful)
        {
            UE_LOG(LogServer, Log, TEXT("Sent message to client: %s"), *Message);
        }
        else
        {
            UE_LOG(LogServer, Error, TEXT("Failed to send message to client"));
        }
    }
    else
    {
        UE_LOG(LogServer, Error, TEXT("No client connected or client disconnected"));
    }
}



void ATCPServer::EndPlay(const EEndPlayReason::Type EndPlayReason)
{
    Super::EndPlay(EndPlayReason);
    CloseTCPListener();
}


bool ATCPServer::CloseTCPListener()
{
    if (ServerSocket)
    {
        ServerSocket->Close();
        ISocketSubsystem::Get(PLATFORM_SOCKETSUBSYSTEM)->DestroySocket(ServerSocket);
        ServerSocket = nullptr;
    }
    if (ClientSocket)
    {
        ClientSocket->Close();
        ISocketSubsystem::Get(PLATFORM_SOCKETSUBSYSTEM)->DestroySocket(ClientSocket);
        ClientSocket = nullptr;
    }

    UE_LOG(LogServer, Log, TEXT("Sockets cleaned up"));
    return true;
}

void ATCPServer::CallBlueprintFunction(TSharedPtr<FJsonObject>& JsonData)
{
    // Assuming `YourBlueprintFunction` is the name of the Blueprint function
    FName FunctionName("pick_up");
    UFunction* Function = FindFunction(FunctionName);

    // character *bp cast 
    // character-->FindINteractableObject
    // Or loop through object manager and find closest object
    // check threshold

    // Function(object)

    FString ObjectID = JsonData->GetStringField("object_id");
    //FString ObjectID = (&JsonData)->GetStringField("object_id");

    // input: object or object_id
    AMyObject* CurrentObjectPtr = ObjectManager->GetObject(ObjectID);

    if (CurrentObjectPtr) {
        FVector Location = CurrentObjectPtr->GetActorLocation();

        if (Function)
        {
            ProcessEvent(Function, nullptr);
        }
    }
    // output: execute animation

}
