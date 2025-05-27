import Phaser from 'phaser';

export default class MainMenu extends Phaser.Scene {
  constructor() {
    super('MainMenu');
  }

  create() {
    const { width, height } = this.sys.game.canvas;

    this.add.text(width / 2, height / 2 - 50, 'BoardGame Hub', {
      fontSize: '48px',
      color: '#222'
    }).setOrigin(0.5);

    const playButton = this.add.text(width / 2, height / 2 + 20, 'Play Game', {
      fontSize: '32px',
      backgroundColor: '#FBB03B',
      color: '#000',
      padding: { left: 20, right: 20, top: 10, bottom: 10 },
      borderRadius: 8
    })
      .setOrigin(0.5)
      .setInteractive({ useHandCursor: true });

    playButton.on('pointerover', () => playButton.setStyle({ backgroundColor: '#FFD966' }));
    playButton.on('pointerout', () => playButton.setStyle({ backgroundColor: '#FBB03B' }));
    playButton.on('pointerdown', () => {
      this.scene.start('MapScene');
    });
  }
}