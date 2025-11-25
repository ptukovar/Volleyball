<template>
  <div class="games-page">
    <h2 class="games-title">Games</h2>
    <ul class="games-list">
      <li v-for="game in games" :key="game.id" class="game-item">
        <a :href="`/games/${game.id}`" class="game-link">
          <div class="game-id">Game #{{ game.id }}</div>
          <div class="game-date">{{ new Date(game.date).toLocaleDateString('en-GB', {
            year: 'numeric', month: 'short', day: 'numeric'
          }) }}</div>
        </a>
      </li>
    </ul>
  </div>
</template>


<script setup>
import { ref, onMounted } from 'vue'

const games = ref([])

async function fetchGames() {
  const res = await fetch('http://localhost:8000/games/')
  games.value = await res.json()
}

onMounted(fetchGames)
</script>

<style scoped>
.games-page {
  max-width: 800px;
  margin: 2rem auto;
  margin-top: 1rem;
  padding: 1rem;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  color: #1f2937;
}

.games-title {
  font-size: 2rem;
  font-weight: 600;
  text-align: center;
  margin-bottom: 1rem;
  color: #111827;
}

.games-list {
  list-style: none;
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
  gap: 1rem;
  padding: 0;
}

.game-item {
  background: #ffffff;
  border-radius: 0.5rem;
  box-shadow: 0 2px 8px rgba(0,0,0,0.05);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}
.game-item:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 16px rgba(0,0,0,0.1);
}

.game-link {
  display: flex;
  flex-direction: column;
  padding: 1rem;
  text-decoration: none;
  color: inherit;
}

.game-id {
  font-size: 1.125rem;
  font-weight: 600;
  margin-bottom: 0.25rem;
  color: #1f2937;
}

.game-date {
  font-size: 0.95rem;
  color: #4b5563;
}

@media (max-width: 600px) {
  .games-page {
    padding: 0.5rem;
  }
  .games-title {
    font-size: 1.5rem;
  }
  .games-list {
    grid-template-columns: 1fr;
  }
}
</style>

