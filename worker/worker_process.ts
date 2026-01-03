import { queue_log } from './websocket_client'; // Assuming we create a client module

function sendLog(logMessage: string) {
    queue_log(logMessage);
}

// Örnek kullanım
sendLog("Worker process started");

// Log göndermek istediğiniz her yerde sendLog fonksiyonunu çağırın
