import PlayerControls from './PlayerControls.js'; // Import PlayerControls for player-specific logic

class GamePhase {
    constructor(players, board) {
        this.players = players; // Array of PlayerControls objects
        this.board = board; // 2D array of HexTileData
        this.currentTurn = 0; // Index of the current player
        this.turnCounter = 0; // Tracks the total number of turns
    }

    // Calculate resources for the current player
    calculateResources(playerId) {
        const player = this.players.find(p => p.playerId === playerId);
        if (!player) throw new Error('Player not found');

        const playerVillages = this.board.flat().filter(tile => {
            return tile.isOccupied && tile.terrainType === 'village' && tile.owner === playerId;
        });

        // Sum up resources based on the tiles the player has villages on
        playerVillages.forEach(tile => {
            const resourceType = tile.resourceType || 'generic'; // Assume each tile has a `resourceType` property
            const resourceAmount = tile.resource || 0; // Assume each tile has a `resource` property
            player.addToCardStack(resourceType, resourceAmount); // Add resources to the player's card stack
        });

        const totalResources = playerVillages.reduce((sum, tile) => {
            return sum + (tile.resource || 0);
        }, 0);

        player.addResources(totalResources); // Use PlayerControls to add resources
        return totalResources;
    }

    // Distribute troops to all players every 4 turns
    distributeTroops() {
        if (this.turnCounter % 4 === 0) {
            this.players.forEach(player => {
                const troopsFromTowns = player.towns.length; // 1 troop per town
                const troopsFromCities = player.cities.length * 2; // 2 troops per city
                const totalTroops = troopsFromTowns + troopsFromCities;

                player.addTroops(totalTroops);
                console.log(`${player.playerName} received ${totalTroops} troops this turn.`);
            });
        }
    }

    // Advance to the next player's turn
    nextTurn() {
        const currentPlayer = this.players[this.currentTurn];

        // Distribute troops every 4 turns
        if (this.currentTurn === 0) {
            this.turnCounter++;
            this.distributeTroops();
        }

        const resourcesGained = this.calculateResources(currentPlayer.playerId);
        console.log(`${currentPlayer.playerName} gained ${resourcesGained} resources this turn.`);

        // Advance to the next player
        this.currentTurn = (this.currentTurn + 1) % this.players.length;
    }

    // Allow the current player to place troops
    placeTroops(playerId, tilePosition, amount) {
        const player = this.players.find(p => p.playerId === playerId);
        if (!player) throw new Error('Player not found');

        player.placeTroops(tilePosition, amount);
    }

    // Get the current player's state
    getCurrentPlayerState() {
        const currentPlayer = this.players[this.currentTurn];
        return currentPlayer.getPlayerState(); // Use PlayerControls to get the player's state
    }

    // Perform an action for the current player
    performAction(action, data) {
        const currentPlayer = this.players[this.currentTurn];
        switch (action) {
            case 'placeVillage':
                currentPlayer.placeVillage(data.position);
                break;
            case 'placeRoad':
                currentPlayer.placeRoad(data.startPosition, data.direction);
                break;
            case 'placeTroops':
                this.placeTroops(currentPlayer.playerId, data.tilePosition, data.amount);
                break;
            default:
                throw new Error('Invalid action');
        }
    }
}

export default GamePhase;