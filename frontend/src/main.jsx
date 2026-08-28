import React, { useState } from 'react';
import { createRoot } from 'react-dom/client';
import { Building2, Send, Sparkles, ExternalLink, Database, ShieldCheck } from 'lucide-react';
import './styles.css';

const prompts = [
  'Show the DarGlobal demo records in Oman.',
  'Show me apartments in Jeddah under 600,000 SAR.',
  'Show the DarGlobal demo luxury residences.',
  'Compare Riyadh and Jeddah options in the collected data.'
];

function App() {
  const [message, setMessage] = useState('');
  const [messages, setMessages] = useState([
    { role: 'assistant', text: 'Ask me about the synthetic DarGlobal/Wasalt-style demo dataset. The records are fictional and are used only to demonstrate retrieval and AI integration.' }
  ]);
  const [loading, setLoading] = useState(false);

  async function submit(text = message) {
    const value = text.trim();
    if (!value || loading) return;
    setMessage('');
    setMessages(prev => [...prev, { role: 'user', text: value }]);
    setLoading(true);
    try {
      const res = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: value })
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || 'Request failed');
      setMessages(prev => [...prev, { role: 'assistant', text: data.answer, sources: data.sources, mode: data.mode }]);
    } catch (err) {
      setMessages(prev => [...prev, { role: 'assistant', text: `I couldn't complete that request: ${err.message}` }]);
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="shell">
      <header className="topbar">
        <div className="brand"><Building2 size={22} /><span>PropertyLens AI</span></div>
        <div className="pill"><span className="dot" /> DarGlobal + Wasalt</div>
      </header>

      <section className="hero">
        <div className="eyebrow"><Sparkles size={15}/> AI-powered property research</div>
        <h1>Property discovery,<br/><em>grounded in real data.</em></h1>
        <p>Explore fictional property records created for a low-risk technical demo of retrieval-augmented AI.</p>
        <div className="trust-row">
          <span><Database size={16}/> Synthetic data</span>
          <span><ShieldCheck size={16}/> Grounded answers</span>
          <span><ExternalLink size={16}/> Reference sites</span>
        </div>
      </section>

      <section className="chat-card">
        <div className="messages">
          {messages.map((m, i) => (
            <div key={i} className={`message ${m.role}`}>
              <div className="bubble">
                <div className="message-label">{m.role === 'assistant' ? 'PropertyLens' : 'You'}</div>
                <div className="message-text">{m.text}</div>
                {m.mode && <div className="mode">{m.mode === 'ai' ? 'AI + retrieval' : 'Retrieval-only mode'}</div>}
                {m.sources?.length > 0 && (
                  <div className="sources">
                    <div className="source-title">Reference sites</div>
                    {m.sources.map((s, j) => (
                      <a href={s.url} target="_blank" rel="noreferrer" key={j}>
                        <span>{s.provider}</span>{s.title}<ExternalLink size={13}/>
                      </a>
                    ))}
                  </div>
                )}
              </div>
            </div>
          ))}
          {loading && <div className="message assistant"><div className="bubble"><div className="thinking"><i/><i/><i/></div></div></div>}
        </div>

        {messages.length <= 1 && (
          <div className="suggestions">
            {prompts.map((p, i) => <button key={i} onClick={() => submit(p)}>{p}</button>)}
          </div>
        )}

        <div className="composer">
          <input
            value={message}
            onChange={e => setMessage(e.target.value)}
            onKeyDown={e => e.key === 'Enter' && submit()}
            placeholder="Ask about projects, cities, prices or property types..."
            maxLength={2000}
          />
          <button aria-label="Send" onClick={() => submit()} disabled={loading || !message.trim()}><Send size={18}/></button>
        </div>
      </section>
      <footer>Synthetic demo dataset only. Records, prices and availability are fictional and must not be treated as real property information.</footer>
    </main>
  );
}

createRoot(document.getElementById('root')).render(<App />);
