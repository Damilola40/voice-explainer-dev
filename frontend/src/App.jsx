import React, {useState} from 'react'
import axios from 'axios'

function App() {
  const [input, setInput] = useState('')
  const [output, setOutput] = useState('')
  const [audioSrc, setAudioSrc] = useState('')

  const handleSubmit = (e) => {
    e.preventDefault()
    // Handle form submission logic here
    async function fetchData() {
      try {
        const response = await axios.post('http://localhost:8000/api/explain/', { user_input: input })
        setOutput(response.data.explanation)
        setAudioSrc(`data:audio/mpeg;base64,${response.data.audio_base64}`)
      } catch (error) {
        console.error('Error generating audio:', error)
        console.error('Error fetching data:', error)
      }
    }
    fetchData()
  }

  return (
    <>
      <section className="container">
        <div className="textarea">
          <form onSubmit={handleSubmit}>
            <textarea id="input" className="input" value={input} onChange={(e) => setInput(e.target.value)}></textarea>
            <button type="submit">Explain</button>
          </form>
        </div>
        <div className="audio">
          {audioSrc && <audio src={audioSrc} controls autoPlay></audio>}
        </div>
        <div className="textOutput">
          <p>{output}</p>
        </div>
      </section>
    </>
  )
}

export default App
