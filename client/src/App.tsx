import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { MessageSquare, Sparkles } from 'lucide-react';
import Chat from './components/Chat';
import ThemeToggle from './components/ThemeToggle';

function App() {
  const [isDark, setIsDark] = useState(true);

  // Apply theme class to document
  useEffect(() => {
    if (isDark) {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  }, [isDark]);

  const toggleTheme = () => setIsDark(!isDark);

  return (
    <div className="min-h-screen bg-gradient-to-br from-light-bg via-light-surface to-light-accent dark:from-dark-bg dark:via-dark-surface dark:to-dark-bg text-light-text dark:text-gray-100">
      {/* Header */}
      <header className="sticky top-0 z-10 backdrop-blur-md bg-light-card/80 dark:bg-dark-card/80 border-b border-light-border dark:border-dark-border">
        <div className="max-w-4xl mx-auto px-4 py-4 flex items-center justify-between">
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            className="flex items-center gap-3"
          >
            <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-neon-blue to-neon-green flex items-center justify-center">
              <MessageSquare className="w-5 h-5 text-white" />
            </div>
            <h1 className="text-xl font-bold bg-gradient-to-r from-neon-blue to-neon-green bg-clip-text text-transparent">
              Azure Chat Lite
            </h1>
            <motion.div
              animate={{ rotate: 360 }}
              transition={{ duration: 3, repeat: Infinity, ease: 'linear' }}
            >
              <Sparkles className="w-5 h-5 text-neon-green" />
            </motion.div>
          </motion.div>
          
          <ThemeToggle isDark={isDark} onToggle={toggleTheme} />
        </div>
      </header>

      {/* Main chat area */}
      <main className="h-[calc(100vh-80px)]">
        <div className="h-full max-w-4xl mx-auto bg-light-card/60 dark:bg-dark-card/60 backdrop-blur-sm border border-light-border dark:border-dark-border rounded-t-3xl shadow-xl">
          <Chat />
        </div>
      </main>
    </div>
  );
}

export default App;
