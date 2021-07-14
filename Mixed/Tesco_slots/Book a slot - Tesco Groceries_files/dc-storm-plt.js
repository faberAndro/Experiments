AWIN.Tracking.basketSubmit = function () {
    var sWhitespaceRegex = /^\s+|\s+$/g;
    var aEncodedLines = new Array();
    AWIN.Tracking.BasketImages = new Array();
    for (var i = 0; i < AWIN.Tracking.Sale.plt.length; i++) {
        var sLine = AWIN.Tracking.Sale.plt[i].replace(sWhitespaceRegex, '');
        if (sLine.length > 0) {
            var aLinePieces = sLine.split('|');
            var sNewLine = '';
            for (var j = 0; j < aLinePieces.length; j++) {
                var sLinePiece = aLinePieces[j].replace(sWhitespaceRegex, '');
                sNewLine += sLinePiece.substring(0, 255) + '|';
            }
            aEncodedLines[aEncodedLines.length] = encodeURIComponent(sNewLine.substring(0, sNewLine.length - 1));
        }
    }
    for (var i = 0; i < aEncodedLines.length; i++) {
        if (aEncodedLines[i].length > 0) {
            AWIN.Tracking.BasketImages[i] = new Image(1,1);
            AWIN.Tracking.BasketImages[i].src = AWIN.sProtocol + 'www.awin1.com/basket.php?product_line=' + aEncodedLines[i];
        }
    }
};

if (AWIN.Tracking.Sale && typeof (AWIN.Tracking.Sale.plt) != 'undefined') {
    if (!document.getElementById('aw_basket') && (typeof (AWIN.Tracking.Sale.plt) === 'object' || typeof (AWIN.Tracking.Sale.plt) === 'array')) {
        AWIN.Tracking.basketSubmit();
    }
}
