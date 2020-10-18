const Discord = require('discord.js');
const { prefix, token } = require('../important/config.json');
const ytdl = require('ytdl-core');

const bot = new Discord.Client();
const queue = new Map();

bot.once('ready', () => {
	console.log('[PRIORITY]musiccmd.js: gBot[JS] is now online.');
});

bot.on('message', async message => {
	if (!message.content.startsWith(prefix) || message.author.bot || message.channel.type === 'dm') return;

	const args = message.content.slice(prefix.length).trim().split(/ +/);
	const command = args.shift().toLowerCase();
	const user = `${message.author.username && message.author.tag}`;
	const serverQueue = queue.get(message.guild.id);

	if (command === 'play' || command === 'p') {
		execute(message, serverQueue);
		console.log(`musiccmd.js: ${user} has executed the command: play`);
		return;
	}
	else if (command === 'skip') {
		skip(message, serverQueue);
		console.log(`musiccmd.js: ${user} has executed the command: skip`);
		return;
	}
	else if (command === 'stop') {
		stop(message, serverQueue);
		console.log(`musiccmd.js: ${user} has executed the command: stop`);
		return;
	}
	else if (command === 'pause') {
		pause(message, serverQueue);
		console.log(`musiccmd.js: ${user} has executed the command: pause`);
		return;
	}
	else if (command === 'resume' || command === 'r') {
		resume(message, serverQueue);
		console.log(`musiccmd.js: ${user} has executed the command: resume`);
		return;
	}
	else if (command === 'clearqueue' || command === 'cq') {
		clear(message, serverQueue);
		console.log(`musiccmd.js: ${user} has executed the command: clearqueue`);
		return;
	}
	else if (command === 'join') {
		joinchannel(message);
		console.log(`musiccmd.js: ${user} has executed the command: join`);
		return;
	}
	else if (command === 'disconnect' || command === 'dc') {
		disconnectchannel(message);
		console.log(`musiccmd.js: ${user} has executed the command: disconnect`);
		return;
	}
});

async function execute(message, serverQueue) {
	const args = message.content.slice(prefix.length).trim().split(/ +/);
	const voiceChannel = message.member.voice.channel;
	const permissions = voiceChannel.permissionsFor(message.client.user);

	if (!voiceChannel) {
		return message.channel.send('You need to be in a voice channel to use this command.');
	}

	if (!permissions.has('CONNECT') || !permissions.has('SPEAK')) {
		return message.channel.send('To use this command, I need the permissions to join and speak.');
	}

	const songInfo = await ytdl.getInfo(args[1]);
	const song = {
		title: songInfo.videoDetails.title,
		url: songInfo.videoDetails.video_url,
	};

	if (!serverQueue) {
		const queueContruct = {
			textChannel: message.channel,
			voiceChannel: voiceChannel,
			connection: null,
			songs: [],
			volume: 5,
			playing: true,
		};

		queue.set(message.guild.id, queueContruct);

		queueContruct.songs.push(song);

		try {
			const connection = await voiceChannel.join();
			queueContruct.connection = connection;
			play(message.guild, queueContruct.songs[0]);
		}
		catch (error) {
			console.log(error);
			queue.delete(message.guild.id);
			return message.channel.send(error);
		}
	}
	else {
		serverQueue.songs.push(song);
		return message.channel.send(`**${song.title}** has been added to the queue.`);
	}
}

function joinchannel(message) {
	const voiceChannel = message.member.voice.channel;
	const permissions = voiceChannel.permissionsFor(message.client.user);

	if (!voiceChannel) {
		return message.channel.send('You need to be in a voice channel to use this command.');
	}
	if (!permissions.has('CONNECT') || !permissions.has('SPEAK')) {
		return message.channel.send('To use this command, I need the permissions to join.');
	}
	voiceChannel.join();
	message.channel.send(`Joined voice channel ${voiceChannel}.`);
}

function disconnectchannel(message) {
	const voiceChannel = message.member.voice.channel;

	if (!voiceChannel) {
		return message.channel.send('You need to be in a voice channel to use this command.');
	}
	voiceChannel.leave();
	message.channel.send(`Disconnected from voice channel ${voiceChannel}.`);
}

function skip(message, serverQueue) {
	if (!message.member.voice.channel) {
		return message.channel.send('You need to be in a voice channel to use this command.');
	}

	if (!serverQueue) {
		return message.channel.send('There is no song to skip.');
	}
	serverQueue.connection.dispatcher.end();
	message.channel.send('Song skipped.');
}

function pause(message, serverQueue) {
	if (!message.member.voice.channel) {
		return message.channel.send('You need to be in a voice channel to use this command.');
	}
	serverQueue.connection.dispatcher.pause();
	message.channel.send('Song paused. To resume, use `/resume`.');
}

function resume(message, serverQueue) {
	if (!message.member.voice.channel) {
		return message.channel.send('You need to be in a voice channel to use this command.');
	}
	serverQueue.connection.dispatcher.resume();
}

function stop(message, serverQueue) {
	if (!message.member.voice.channel) {
		return message.channel.send('You need to be in a voice channel to use this command.');
	}
	serverQueue.connection.dispatcher.end();
	serverQueue.songs = [];
	message.channel.send('Song stopped.');
}

function clear(message, serverQueue) {
	if (!message.member.voice.channel) {
		return message.channel.send('You need to be in a voice channel to use this command.');
	}
	serverQueue.songs = [];
	message.channel.send('Queue cleared.');
}

function play(guild, song) {
	const serverQueue = queue.get(guild.id);
	if (!song) {
		serverQueue.voiceChannel.leave();
		queue.delete(guild.id);
		return;
	}

	const dispatcher = serverQueue.connection
		.play(ytdl(song.url))
		.on('finish', () => {
			serverQueue.songs.shift();
			play(guild, serverQueue.songs[0]);
		})
		.on('error', error => console.error(error));
	dispatcher.setVolumeLogarithmic(serverQueue.volume / 5);
	serverQueue.textChannel.send(`Now Playing: **${song.title}**`);
}

bot.login(token);