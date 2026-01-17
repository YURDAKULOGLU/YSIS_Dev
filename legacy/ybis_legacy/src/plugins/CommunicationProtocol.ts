export interface CommunicationProtocol {
    sendMessage(message: string, recipient: string): Promise<void>;
    receiveMessage(): Promise<string>;
}
