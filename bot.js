// bot.js
const TelegramBot = require('node-telegram-bot-api');
const fs = require('fs');
const whitelist = require('./whitelist.json');
const axios = require('axios');

const token = 'YOUR_BOT_TOKEN';
const bot = new TelegramBot(token, { polling: true });

function isWhitelisted(userId) {
    return whitelist.includes(userId);
}

const mainMenu = {
    reply_markup: {
        inline_keyboard: [
            [{ text: 'Email Tools', callback_data: 'email' }],
            [{ text: 'Username Lookup', callback_data: 'username' }],
            [{ text: 'Phone Number', callback_data: 'phone' }],
            [{ text: 'IP Address', callback_data: 'ip' }],
            [{ text: 'Domain Info', callback_data: 'domain' }],
            [{ text: 'Social Media', callback_data: 'social' }],
            [{ text: 'Image/Metadata', callback_data: 'image' }],
            [{ text: 'Dark Web', callback_data: 'darkweb' }],
            [{ text: 'Leaks & Breaches', callback_data: 'leak' }],
            [{ text: 'Geolocation', callback_data: 'geo' }],
            [{ text: 'Pentest Tools', callback_data: 'pentest' }]
        ]
    }
};

bot.onText(/\/start/, (msg) => {
    const chatId = msg.chat.id;
    if (!isWhitelisted(chatId)) {
        return bot.sendMessage(chatId, 'Access denied. You are not whitelisted.');
    }
    bot.sendMessage(chatId, 'Welcome to OSINT Bot. Choose a category:', mainMenu);
});

bot.on('callback_query', (query) => {
    const chatId = query.message.chat.id;
    const category = query.data;

    if (!isWhitelisted(chatId)) return;

    let response = {
        email: "Email OSINT Tools:\\n- haveibeenpwned.com\\n- emailrep.io\\n- hunter.io",
        username: "Username Lookup:\\n- namechk.com\\n- whatsmyname.app\\n- sherlock",
        phone: "Phone Trackers:\\n- numverify.com\\n- truecaller.com\\n- phoneinfoga",
        ip: "IP OSINT:\\n- ipinfo.io\\n- shodan.io\\n- abuseipdb.com",
        domain: "Domain Tools:\\n- whois\\n- crt.sh\\n- dnsdumpster.com",
        social: "Social Media OSINT:\\n- Telegram Lookup\\n- Facebook Graph\\n- Twitter Search",
        image: "Image Metadata:\\n- exif viewer\\n- fotoforensics.com\\n- reverse image search",
        darkweb: "Dark Web:\\n- ahmia.fi\\n- onion.live\\n- hidden wiki",
        leak: "Data Breach Tools:\\n- leakcheck.io\\n- snusbase\\n- weleakinfo (mirror)",
        geo: "Geolocation Tools:\\n- exif GPS\\n- cell tower lookup\\n- google timeline",
        pentest: "Pentest Tools:\\n- nmap\\n- recon-ng\\n- harvester\\n- dork generator"
    }[category] || "Unknown category";

    bot.sendMessage(chatId, response);
});

// Cek email reputasi
bot.onText(/\/email (.+)/, (msg, match) => {
    const email = match[1];
    const chatId = msg.chat.id;

    const url = `https://emailrep.io/${email}`;
    const headers = { 'Key': 'API_KEY_EMAILREP' };

    axios.get(url, { headers })
        .then((response) => {
            const res = response.data;
            const result = `
Email: ${res.email || 'n/a'}
Reputation: ${res.reputation || 'n/a'}
Suspicious: ${res.suspicious || 'n/a'}
Blacklisted: ${res.blacklisted || 'n/a'}
Sources: ${res.sources.join(', ') || 'n/a'}
            `;
            bot.sendMessage(chatId, result);
        })
        .catch((error) => {
            bot.sendMessage(chatId, 'Error fetching email data.');
        });
});

bot.onText(/\/history/, (msg) => {
    const chatId = msg.chat.id;
    fs.readFile('history.log', 'utf8', (err, data) => {
        if (err) {
            bot.sendMessage(chatId, 'No history available.');
            return;
        }
        bot.sendMessage(chatId, 'Recent History:\n' + data.split('\n').slice(-10).join('\n'));
    });
});
