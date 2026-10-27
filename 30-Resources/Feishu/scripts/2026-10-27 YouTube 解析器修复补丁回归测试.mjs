import fs from 'fs';
const html = fs.readFileSync('/tmp/yt.html','utf8');
function parseYouTubePageData(html) {
  const videos = [];
  const m = html.match(/var\s+ytInitialData\s*=\s*({[\s\S]*?});\s*<\/script>/);
  if (!m) return videos;
  let data; try { data = JSON.parse(m[1]); } catch { return videos; }
  const tabs = data?.contents?.twoColumnBrowseResultsRenderer?.tabs || [];
  for (const tab of tabs) {
    const gridItems = tab?.tabRenderer?.content?.richGridRenderer?.contents || [];
    for (const it of gridItems) {
      const v = it?.richItemRenderer?.content?.videoRenderer;
      if (v?.videoId) { videos.push({title: v.title?.runs?.[0]?.text||v.title?.simpleText||'', url:`https://www.youtube.com/watch?v=${v.videoId}`}); }
      const lv = it?.richItemRenderer?.content?.lockupViewModel;
      if (lv?.contentId) {
        const title = lv?.metadata?.lockupMetadataViewModel?.title?.content || '';
        if (title) videos.push({title, url:`https://www.youtube.com/watch?v=${lv.contentId}`});
      }
    }
    if (videos.length > 0) break;
    const playlistItems = tab?.tabRenderer?.content?.sectionListRenderer?.contents?.[0]?.itemSectionRenderer?.contents?.[0]?.playlistVideoListRenderer?.contents || [];
    for (const it of playlistItems) {
      const v = it?.playlistVideoRenderer;
      if (v?.videoId) { videos.push({title: v.title?.runs?.[0]?.text||v.title?.simpleText||'', url:`https://www.youtube.com/watch?v=${v.videoId}`}); }
    }
    if (videos.length > 0) break;
  }
  return videos;
}
const v = parseYouTubePageData(html);
console.log('PATCHED parser result:', v.length, 'videos');
for (const x of v.slice(0,6)) console.log('  -', x.title.slice(0,60), '|', x.url);
const target = v.find(x => x.title.includes('Changing Physics of Cybersecurity'));
console.log('TARGET MATCH:', target ? target.url : 'NOT FOUND');
