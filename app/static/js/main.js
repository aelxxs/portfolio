import { render } from "https://cdn.skypack.dev/million";
import { html } from "https://cdn.skypack.dev/million/html";

// ---

const battery = document.querySelector(".battery");
const discord = document.querySelector(".discord");

const renderBatteryStatus = (kv) => {
	const status = JSON.parse(kv.battery);

	render(battery, html`<p>Laptop Status: 💻 » ${status.isCharging ? "⚡" : "🔋"} ${status.percentage}%</p>`);
};

const renderDiscordStatus = (vscode) => {
	const getTimeElapsed = () => {
		const currentTime = Date.now();

		const timeElapsed = Math.abs(currentTime - vscode.timestamps.start) / 1000;
		const timeElapsedArray = [
			Math.floor(timeElapsed / 3600) % 24,
			Math.floor(timeElapsed / 60) % 60,
			Math.floor(timeElapsed % 60),
		];

		if (timeElapsedArray[0] === 0) {
			timeElapsedArray.shift();
		}

		const format = (time) => `0${time}`.slice(-2);

		return `${timeElapsedArray.map(format).join(":")} elapsed`;
	};

	const image = vscode.assets.large_image.startsWith("mp:external")
		? vscode.assets.large_image.replace(/mp:external\/([^\/]*)\/(http[s])/g, "$2:/")
		: `https://cdn.discordapp.com/app-assets/${vscode.application_id}/${vscode.assets.large_image}.webp`;

	const card = html`
        <div class="presence-card">
            <img class="card__icon" src="${image}"></img>
            <div class="card__body">
                <div class="card__header">
                    <h4>${vscode.name}</h4>
                </div>
                <div class="card__text">
                    <span>${vscode.details}</span>
                    <span>${vscode.state}</span>
                    <div class="counter">
                        <span>Time: ${getTimeElapsed()}</span>
                    </div>
                </div>
            </div>
        </div>
    `;

	render(discord, card);

	const counter = document.querySelector(".counter");

	setInterval(() => {
		render(counter, html`<span>Time: ${getTimeElapsed()}</span>`);
	}, 10);
};

lanyard({
	userId: "406665840088317962",
	socket: true,
	onPresenceUpdate: ({ activities, kv }) => {
		const vscode = activities.find((activity) => activity.application_id == "810516608442695700");

		if (vscode) {
			renderDiscordStatus(vscode);
		}

		renderBatteryStatus(kv);
	},
});

const lastfm = document.querySelector(".lastfm");

const renderCurrentSong = async () => {
	const data = await fetch("/api/now_playing");

	const { song } = await data.json();

	if (song) {
		const song = html`
			<a href="${song.url}" target="_blank">
				<div class="song-card">
					<img class="card__icon" src="${song.cover}" />
					<div class="card__body">
						<div class="card__header">
							<span span class="song__name" title="${song.name}">${song.name}</span>
						</div>
						<div class="card__footer">
							<span class="song__artist">${song.artist}</span>
							<div class="song__now-playing">
								<span></span>
								<span></span>
								<span></span>
							</div>
						</div>
					</div>
				</div>
			</a>
		`;

		render(lastfm, song);
	}
};

renderCurrentSong();
setInterval(async () => {
	await renderCurrentSong();
}, 5000);
