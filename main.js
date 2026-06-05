const { app, BrowserWindow, dialog, ipcMain } = require('electron');

function createWindow() {
    const win = new BrowserWindow({
        width: 900,
        height: 600,
        backgroundColor: '#f0f8ff',
        webPreferences: {
            nodeIntegration: true,
            contextIsolation: false
        }
    });
    win.loadFile('index.html');
}

app.whenReady().then(createWindow);

// IPC dinleyicisi - renderer'dan gelen "show-prompt" mesajını yakala
ipcMain.on('show-prompt', (event, args) => {
    const win = BrowserWindow.fromWebContents(event.sender);
    dialog.showMessageBox(win, {
        type: 'question',
        buttons: ['Tamam', 'İptal'],
        title: 'Yeni Profil',
        message: 'Profil adı girin:',
        defaultId: 0,
        cancelId: 1
    }).then(result => {
        // Burada input almak için normal dialog yeterli değil
        // İkinci aşamada custom prompt yapacağız
        event.reply('prompt-result', result.response === 0 ? 'test_profil' : null);
    });
});

// Basit mesaj kutusu için
ipcMain.on('show-message', (event, args) => {
    const win = BrowserWindow.fromWebContents(event.sender);
    dialog.showMessageBox(win, {
        type: 'info',
        title: 'Bilgi',
        message: args.message
    });
});