class PlayerControls {
    constructor(playerId, playerName) {
        this.playerId = playerId; // Unique ID for the player
        this.playerName = playerName; // Name of the player
        this.resources = 0; // Tracks the player's resources
        this.villages = []; // Tracks the positions of villages owned by the player
        this.roads = []; // Tracks the positions of roads owned by the player
        this.cardStack = []; // Tracks the player's resource cards
        this.towns = []; // Tracks the positions of towns owned by the player
        this.cities = []; // Tracks the positions of cities owned by the player
        this.troops = 0; // Tracks the player's total troops
    }

    // Add troops to the player
    addTroops(amount) {
        this.troops += amount;
        console.log(`${this.playerName} now has ${this.troops} troops.`);
    }

    // Place troops on a specific tile
    placeTroops(tilePosition, amount) {
        const isTownOrCity = this.towns.some(town => town.x === tilePosition.x && town.y === tilePosition.y) ||
            this.cities.some(city => city.x === tilePosition.x && city.y === tilePosition.y);

        if (!isTownOrCity) {
            throw new Error(`${this.playerName} can only place troops on their towns or cities.`);
        }

        if (amount > this.troops) {
            throw new Error(`${this.playerName} does not have enough troops to place.`);
        }

        this.troops -= amount;
        console.log(`${this.playerName} placed ${amount} troops on tile ${JSON.stringify(tilePosition)}.`);
    }

    // Add a town for the player
    addTown(position) {
        this.towns.push(position);
        console.log(`${this.playerName} added a town at ${JSON.stringify(position)}.`);
    }

    // Add a city for the player
    addCity(position) {
        this.cities.push(position);
        console.log(`${this.playerName} added a city at ${JSON.stringify(position)}.`);
    }

    // Get the player's current state
    getPlayerState() {
        return {
            playerId: this.playerId,
            playerName: this.playerName,
            resources: this.resources,
            villages: this.villages,
            roads: this.roads,
            cardStack: this.cardStack,
            towns: this.towns,
            cities: this.cities,
            troops: this.troops
        };
    }
}

export default PlayerControls;