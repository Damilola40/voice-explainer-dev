import React, {useState} from 'react'
import axios from 'axios'
import './App.css'

function App() {
  const [input, setInput] = useState('')
  const [output, setOutput] = useState('')
  const [audioSrc, setAudioSrc] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [errorMsg, setErrorMsg] = useState('')

  const handleSubmit = (e) => {
    e.preventDefault()
    // Handle form submission logic here
    async function fetchData() {
      try {
        setIsLoading(true)
        setErrorMsg('')
        const response = await axios.post('http://localhost:8000/api/explain/', { user_input: input })
        setOutput(response.data.explanation)
        setAudioSrc(`data:audio/mpeg;base64,${response.data.audio_base64}`)
      } catch (error) {
        setErrorMsg('Something went wrong — please try again.')
      } finally {
        setIsLoading(false)
      }
    }
    fetchData()
  }

  return (
  <>
    <section className="container">
      <h1 className="brand">Voxplain</h1>
      <p className="tagline">Ask anything. Hear it explained.</p>
      <div className="textarea">
        <form onSubmit={handleSubmit}>
          <textarea id="input" className="input" value={input} onChange={(e) => setInput(e.target.value)} placeholder="Paste your code, error, or question..."></textarea>
          <button type="submit" disabled={isLoading}>
            {isLoading ? 'Thinking...' : 'Explain'}
          </button>
        </form>
      </div>
      {errorMsg && <p className="error">{errorMsg}</p>}
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
