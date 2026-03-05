module.exports = {
  apps: [{
    name: 'SimpleApplicationBot',
    script: 'main.py',
    interpreter: './venv/bin/python',
    max_memory_restart: '200M',
  }]
};