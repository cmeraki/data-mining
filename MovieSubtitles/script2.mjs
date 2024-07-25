import fetch from 'node-fetch';

// Get the film_name from command-line arguments
const filmName = process.argv[2];

if (!filmName) {
  console.error('Please provide a film name.');
  process.exit(1);
}

const apiKey = '_g5OPL9jJO3a_oD6Qd9r60LF0_dmM5Nl';
const url = `https://api.subdl.com/api/v1/subtitles?api_key=${apiKey}&film_name=${encodeURIComponent(filmName)}&type=movie&languages=en`;

fetch(url, {
  method: "GET",
  headers: {
    "Accept": "application/json"
  }
})
.then(response => response.json())
.then(data => {
  // Find the first English subtitle
  const firstEnglishSubtitle = data.subtitles.find(subtitle => subtitle.lang === 'english');
  
  if (firstEnglishSubtitle) {
    // Extract the URL
    const subtitleUrl = firstEnglishSubtitle.url;
    console.log(subtitleUrl);
  } else {
    console.log('No English subtitles found.');
  }
})
.catch(error => console.error('Error:', error));
