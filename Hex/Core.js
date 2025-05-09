import GamePhase from './GamePhase.js'; // Import the GamePhase class

class GameCore {
    constructor(players, board) {
        this.players = players; // Array of player objects
        this.board = board; // 2D array of HexTileData
        this.currentTurn = 0; // Index of the current player
        this.placedVillages = {}; // Tracks placed villages by player
        this.placedRoads = {}; // Tracks placed roads by player
        this.gamePhase = 'setup'; // Tracks the current phase: 'setup' or 'game'
        this.gamePhaseHandler = null; // Will hold the GamePhase instance
    }

    // Initialize the game state
    initializeGame() {
        this.players.forEach(player => {
            this.placedVillages[player.playerId] = 0; // Each player starts with 0 villages placed
            this.placedRoads[player.playerId] = 0; // Each player starts with 0 roads placed
        });
    }

    // Place a village on a hex tile
    placeVillage(playerId, tilePosition) {
        if (this.gamePhase !== 'setup') throw new Error('Villages can only be placed during the setup phase');

        const player = this.players.find(p => p.playerId === playerId);
        if (!player) throw new Error('Player not found');

        const tile = this.getTile(tilePosition);
        if (!tile) throw new Error('Invalid tile position');
        if (tile.isOccupied) throw new Error('Tile is already occupied');
        if (this.placedVillages[playerId] >= 2) throw new Error('Player has already placed 2 villages');

        // Place the village
        tile.isOccupied = true;
        tile.terrainType = 'village'; // Mark the tile as a village
        this.placedVillages[playerId]++;

        this.checkSetupCompletion(); // Check if the setup phase is complete

        return tile;
    }

    // Place a road connecting two tiles
    placeRoad(playerId, startTilePosition, endTilePosition) {
        if (this.gamePhase !== 'setup') throw new Error('Roads can only be placed during the setup phase');

        const player = this.players.find(p => p.playerId === playerId);
        if (!player) throw new Error('Player not found');

        const startTile = this.getTile(startTilePosition);
        const endTile = this.getTile(endTilePosition);

        if (!startTile || !endTile) throw new Error('Invalid tile position');
        if (!startTile.isOccupied || startTile.terrainType !== 'village') {
            throw new Error('Road must start from a village');
        }
        if (this.calculateDistance(startTilePosition, endTilePosition) !== 1) {
            throw new Error('Road must connect adjacent tiles');
        }
        if (this.placedRoads[playerId] >= 2) throw new Error('Player has already placed 2 roads');

        // Place the road
        startTile.roads = startTile.roads || [];
        startTile.roads.push(endTilePosition);
        this.placedRoads[playerId]++;

        this.checkSetupCompletion(); // Check if the setup phase is complete

        return { startTile, endTile };
    }

    // Check if all players have completed their setup
    checkSetupCompletion() {
        const allVillagesPlaced = this.players.every(player => this.placedVillages[player.playerId] === 2);
        const allRoadsPlaced = this.players.every(player => this.placedRoads[player.playerId] === 2);

        if (allVillagesPlaced && allRoadsPlaced) {
            this.transitionToGamePhase();
        }
    }

    // Transition to the game phase
    transitionToGamePhase() {
        this.gamePhase = 'game';
        this.gamePhaseHandler = new GamePhase(this.players, this.board); // Initialize GamePhase
        console.log('The game phase has started!');
    }

    // Delegate turn management to GamePhase
    nextTurn() {
        if (this.gamePhase === 'game') {
            this.gamePhaseHandler.nextTurn(); // Delegate to GamePhase
        } else {
            this.currentTurn = (this.currentTurn + 1) % this.players.length;
        }
    }

    // Helper to get a tile by position
    getTile(position) {
        const { x, y } = position;
        return this.board[x] && this.board[x][y] ? this.board[x][y] : null;
    }

    // Helper to calculate distance between two tiles on a hexagonal grid
    calculateDistance(pos1, pos2) {
        const dx = pos1.x - pos2.x;
        const dy = pos1.y - pos2.y;
        const dz = -(dx + dy); // Cube coordinate z is derived as -(x + y)
        return Math.max(Math.abs(dx), Math.abs(dy), Math.abs(dz));
    }
}

export default GameCore;

