/* eslint-disable */
const iframe = '<div class="videoWrapper"><iframe src="%1" width="%2" height="%3" frameborder="0" allowfullscreen></iframe></div>';

const imgRegex = /(?:<p>)?<img.*?src="(.+?)"(.*?)\/?>(?:<\/p>)?/gi;

const fullYoutubeRegex = /(?:(?:https?:)?(?:\/\/)?)(?:(?:www)?\.)?youtube\.(?:.+?)\/(?:(?:watch\?v=)|(?:embed\/))([a-zA-Z0-9_-]{11})/i;

const shortYoutubeRegex = /(?:(?:https?:)?(?:\/\/)?)?youtu\.be\/([a-zA-Z0-9_-]{11})/i;

function parseDimensions(rest, options) {
  var width,
    height,
    d,
    defaultWidth,
    defaultHeight;

  defaultWidth = options.youtubeWidth ? options.youtubeWidth : 420;
  defaultHeight = options.youtubeHeight ? options.youtubeHeight : 315;

  if (rest) {
    width = (d = /width="(.+?)"/.exec(rest)) ? d[1] : defaultWidth;
    height = (d = /height="(.+?)"/.exec(rest)) ? d[1] : defaultHeight;
  }

  // add units so they can be used in css
  if (/^\d+$/gm.exec(width)) {
    width += 'px';
  }
  if (/^\d+$/gm.exec(height)) {
    height += 'px';
  }

  return { width, height };
}

function youtubeExt() {
  return [{
    type: 'output',
    filter: function (text, converter, options) {
      var tag = iframe;
      return text.replace(imgRegex, function (match, url, rest) {
        var d = parseDimensions(rest, options),
          m, fUrl = '';
        if ((m = shortYoutubeRegex.exec(url)) || (m = fullYoutubeRegex.exec(url))) {
          fUrl = 'https://www.youtube.com/embed/' + m[1] + '?rel=0';
          if (options.youtubejsapi) {
            fUrl += '&enablejsapi=1';
          }
        } else {
          return match;
        }
        return tag.replace(/%1/g, fUrl).replace('%2', d.width).replace('%3', d.height);
      });
    },
  }];
}

export default youtubeExt;
