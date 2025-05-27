import MainMenu from './MainMenu.js';
import MapScene from './MapScene.js';

const config = {
  type: Phaser.AUTO,
  width: 1000,
  height: 1000,
  scene: [MainMenu, MapScene],
  parent: 'game-container',
  backgroundColor: '#fff'
};

new Phaser.Game(config);