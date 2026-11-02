// Render exact video-title typography; FFmpeg places the existing logo in the video.
import Foundation
import CoreGraphics
import CoreText
import ImageIO
let titles = [
    "white-noise": "Softened white noise",
    "distant-thunder-rain": "Distant thunder and steady rain",
    "rain-on-window": "Gentle rain on a window",
    "brown-noise": "Deep brown noise",
    "ambient-drone": "Deep ambient sleep drone"
]
let destination = CommandLine.arguments[1]
for (kind, title) in titles {
    let context = CGContext(data: nil, width: 1280, height: 720, bitsPerComponent: 8,
        bytesPerRow: 1280*4, space: CGColorSpaceCreateDeviceRGB(),
        bitmapInfo: CGImageAlphaInfo.noneSkipLast.rawValue)!
    context.setFillColor(CGColor(gray: 0, alpha: 1))
    context.fill(CGRect(x: 0, y: 0, width: 1280, height: 720))
    let attributes: [NSAttributedString.Key: Any] = [
        NSAttributedString.Key(kCTFontAttributeName as String): CTFontCreateWithName("Helvetica" as CFString, 48, nil),
        NSAttributedString.Key(kCTForegroundColorAttributeName as String): CGColor(red: 0.90, green: 0.88, blue: 0.84, alpha: 1)
    ]
    let line = CTLineCreateWithAttributedString(NSAttributedString(string: title, attributes: attributes))
    let width = CTLineGetTypographicBounds(line, nil, nil, nil)
    context.textPosition = CGPoint(x: (1280-width)/2, y: 410)
    CTLineDraw(line, context)
    let url = URL(fileURLWithPath: "\(destination)/\(kind)-text.png")
    let output = CGImageDestinationCreateWithURL(url as CFURL, "public.png" as CFString, 1, nil)!
    CGImageDestinationAddImage(output, context.makeImage()!, nil)
    guard CGImageDestinationFinalize(output) else { fatalError("Cannot write title") }
}
