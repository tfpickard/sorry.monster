export function Header() {
  return (
    <header className="border-b border-slate-200 dark:border-slate-700 bg-white/50 dark:bg-slate-900/50 backdrop-blur">
      <div className="container mx-auto px-4 py-4 flex justify-between items-center">
        <div className="flex items-center space-x-4">
          <span className="text-2xl font-bold">sorry.monster</span>
        </div>
        <nav className="flex items-center space-x-4">
          <a
            href="/docs"
            className="text-sm text-slate-600 dark:text-slate-300 hover:text-slate-900 dark:hover:text-white"
          >
            API Docs
          </a>
          <a
            href="https://oops.ninja"
            className="text-sm bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700"
            target="_blank"
            rel="noopener noreferrer"
          >
            Try oops.ninja
          </a>
        </nav>
      </div>
    </header>
  );
}
