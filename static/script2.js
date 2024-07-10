async function convertName() {
  const input = document.getElementById('nameInput').value.trim();
  try {
    const response = await axios.post(
      'http://127.0.0.1:3000//convert-name',
      { name: input },
      {
        headers: {
          'Content-Type': 'application/json',
        },
      }
    );

    // Log the raw response for debugging
    console.log('Raw response:', response.data);

    // Parse the JSON string in the response
    let data;
    if (typeof response.data.result === 'string') {
      const jsonString = response.data.result.replace(/```json\n|\n```/g, '');
      data = JSON.parse(jsonString);
    } else {
      data = response.data.result;
    }

    console.log('Parsed data:', data);

    if (data && data.final_name) {
      document.getElementById('result').innerHTML = `
        <p><strong>Original Name:</strong> ${data.original_name || 'N/A'}</p>
        <p><strong>Name Meaning:</strong> ${data.name_meaning || 'N/A'}</p>
        <p><strong>Japanese Translation:</strong> ${
          data.japanese_translation || 'N/A'
        }</p>
        <p><strong>Final Name:</strong></p>
        <ul>
          <li><strong>Romaji:</strong> ${data.final_name.romaji || 'N/A'}</li>
          <li><strong>Kanji:</strong> ${data.final_name.kanji || 'N/A'}</li>
          <li><strong>Hiragana:</strong> ${
            data.final_name.hiragana || 'N/A'
          }</li>
          <li><strong>Meaning in English:</strong> ${
            data.final_name['meaning in english'] || 'N/A'
          }</li>
        </ul>
      `;

      document.getElementById('playButton').disabled = !data.final_name.romaji;

      if (response.data.warnings && response.data.warnings.length > 0) {
        document.getElementById('warnings').innerHTML = `
          <p class="warning">${response.data.warnings.join('<br>')}</p>
        `;
      } else {
        document.getElementById('warnings').innerHTML = '';
      }
    } else {
      throw new Error('Invalid response format');
    }
  } catch (error) {
    console.error('Error converting name:', error);
    alert('Sorry, there was an error converting the name. Please try again.');
  }
}

async function playAudio() {
  const resultDiv = document.getElementById('result');
  const romajiElement = resultDiv.querySelector('li:nth-child(1)');

  if (!romajiElement) {
    alert('No name to pronounce. Please convert a name first.');
    return;
  }

  const romaji = romajiElement.textContent.split(':')[1].trim();

  try {
    const response = await axios.get(
      `https://api.streamelements.com/kappa/v2/speech?voice=ja-JP-Standard-A&text=${encodeURIComponent(
        romaji
      )}`,
      {
        responseType: 'blob',
      }
    );
    const audioBlob = new Blob([response.data], { type: 'audio/mpeg' });
    const audioUrl = URL.createObjectURL(audioBlob);
    const audioPlayer = document.getElementById('audioPlayer');
    audioPlayer.src = audioUrl;
    audioPlayer.play();
  } catch (error) {
    console.error('Error playing audio:', error);
    alert('Sorry, there was an error playing the audio. Please try again.');
  }
}
