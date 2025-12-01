const { desktopCapturer, screen } = require('electron');
const sharp = require('sharp');

class ScreenshotService {
    async captureFullScreen() {
        try {
            const sources = await desktopCapturer.getSources({
                types: ['screen'],
                thumbnailSize: screen.getPrimaryDisplay().size
            });

            if (sources.length === 0) {
                throw new Error('No se pudo capturar la pantalla');
            }

            return sources[0].thumbnail.toPNG();
        } catch (error) {
            console.error('Error capturing screen:', error);
            throw error;
        }
    }

    async cropImage(imageBuffer, bounds) {
        try {
            const display = screen.getPrimaryDisplay();
            const metadata = await sharp(imageBuffer).metadata();
            
            const scaleX = metadata.width / display.size.width;
            const scaleY = metadata.height / display.size.height;

            const cropBounds = {
                left: Math.max(0, Math.round(bounds.x * scaleX)),
                top: Math.max(0, Math.round(bounds.y * scaleY)),
                width: Math.round(bounds.width * scaleX),
                height: Math.round(bounds.height * scaleY)
            };

            if (cropBounds.left + cropBounds.width > metadata.width) {
                cropBounds.width = metadata.width - cropBounds.left;
            }
            if (cropBounds.top + cropBounds.height > metadata.height) {
                cropBounds.height = metadata.height - cropBounds.top;
            }

            return await sharp(imageBuffer)
                .extract(cropBounds)
                .png({ quality: 90 })
                .toBuffer();
        } catch (error) {
            console.error('Error cropping image:', error);
            throw error;
        }
    }

    imageToBase64(buffer) {
        const base64 = buffer.toString('base64');
        return `data:image/png;base64,${base64}`;
    }
}

module.exports = new ScreenshotService();