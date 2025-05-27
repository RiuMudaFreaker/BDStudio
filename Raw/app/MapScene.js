import Phaser from 'phaser';

// Helper: Convert SVG path "M x1,y1 L x2,y2 ... Z" to array of [x, y]
function svgPathToPoints(d) {
  return d
    .replace(/[A-Za-z]/g, '') // Remove M, L, Z
    .trim()
    .split(/\s+/)
    .map(pair => pair.split(',').map(Number));
}

// Example regions; replace with your real SVG path data
const regions = [
  { id: 'region-1', d: 'M100,100 L200,100 L200,200 L100,200 Z', fill: 0x736357 },
  { id: 'region-2', d: 'M300,100 L400,100 L400,200 L300,200 Z', fill: 0x534741 },
];

export default class MapScene extends Phaser.Scene {
  constructor() {
    super('MapScene');
  }

  create() {
    regions.forEach(region => {
      const points = svgPathToPoints(region.d);
      const flatPoints = points.flat();

      // Draw region as a polygon
      const poly = this.add.polygon(0, 0, flatPoints, region.fill, 1)
        .setOrigin(0)
        .setInteractive({ useHandCursor: true });

      // Hover effect
      poly.on('pointerover', () => {
        poly.setFillStyle(region.fill, 0.6);
      });
      poly.on('pointerout', () => {
        poly.setFillStyle(region.fill, 1);
      });

      // Click effect
      poly.on('pointerdown', () => {
        poly.setFillStyle(0xff0000, 1);
        this.add.text(poly.x + 10, poly.y + 10, `Clicked: ${region.id}`, { color: '#000', fontSize: 16 });
      });
    });
  }
}