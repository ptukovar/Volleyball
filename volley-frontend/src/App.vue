<template>
  <div id="app">
    <nav class="navbar">
      <ul class="nav-list">
        <li class="nav-item"><router-link class="nav-link" to="/">Home</router-link></li>
        <li class="nav-item"><router-link class="nav-link" to="/players">Players</router-link></li>
        <li class="nav-item"><router-link class="nav-link" to="/games">Games</router-link></li>
        <li class="nav-item"><router-link class="nav-link" to="/new-player">New Player</router-link></li>
        <li class="nav-item"><router-link class="nav-link" to="/new-game">New Game</router-link></li>
      </ul>
    </nav>
    <router-view/>
  </div>
  <footer>Marek Pukowiec</footer>
</template>



<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}
footer {
  text-align: center;
  padding: 1rem;
  background-color: #1f2937;
  color: #f9fafb;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  position: fixed;
  width: 100%;
  bottom: 0;
}

.navbar {
  background-color: #1f2937;
  padding: 0 2rem;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  box-shadow: 0 2px 5px rgba(0,0,0,0.2);
}

.nav-list {
  list-style: none;
  display: flex;
  align-items: center;
  height: 4rem;
  justify-content: center;
}

.nav-item {
  margin-right: 1.5rem;
}

.nav-link {
  text-decoration: none;
  color: #f9fafb; 
  font-size: 1rem;
  font-weight: 500;
  position: relative;
  padding: 0.5rem 0;
  transition: color 0.3s ease;
}

.nav-link:hover {
  color: #3b82f6; 
}

.router-link-active.nav-link::after {
  content: '';
  position: absolute;
  left: 0;
  bottom: -0.2rem;
  width: 100%;
  height: 3px;
  background-color: #3b82f6;
  border-radius: 2px;
}

.nav-item:last-child {
  margin-right: 0;
}

@media (max-width: 768px) {
  .nav-list {
    flex-direction: column;
    background-color: #1f2937;
    position: absolute;
    top: 4rem;
    left: 0;
    width: 100%;
    transform: translateY(-100%);
    transition: transform 0.3s ease;
  }
  .nav-list.open {
    transform: translateY(0);
  }
  .nav-item {
    margin: 1rem 0;
    text-align: center;
  }
  .navbar::before {
    content: '☰';
    font-size: 1.5rem;
    color: #f9fafb;
    cursor: pointer;
    position: absolute;
    right: 2rem;
    top: 1.2rem;
  }
}
</style>

