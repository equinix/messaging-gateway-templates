'use strict';
//Below configurations will be issued to customer offline as part of on-boarding process.
module.exports = {
    EQUINIX_OUTGOING_QUEUE: 'uat_e_queue',
    EQUINIX_OUTGOING_QUEUE_CONNECTION_STRING: 'Endpoint=sb://eqixsvcbus.servicebus.windows.net/;SharedAccessKeyName=uat_listenonly;SharedAccessKey=NJQ3PB9h9H9ArZTenp3JeXvqZ9jnDiZWVOLKBSUG07o=;EntityPath=uat_e_queue',
    FILE_STORAGE_KEY : '<FILE_STORAGE_KEY>'
}
