<template>
  <div class="players-page">
    <h2 class="players-title">Players</h2>
    <div class="players-grid">
      <div v-for="p in players" :key="p.id" class="player-card">
        <a :href="`/players/${p.id}`" class="player-link">
          <div class="player-image-wrapper">
            <img :src="p.image" alt="Player Image" class="player-image" />
          </div>
          <div class="player-info">
            <div class="player-nickname">{{ p.nickname }}</div>
            <div class="player-name">{{ p.first_name }} {{ p.last_name }}</div>
          </div>
        </a>
      </div>
    </div>
  </div>
</template>


<script setup>
import { ref, onMounted } from 'vue'

const players = ref([])

async function fetchPlayers() {
  const res = await fetch('http://localhost:8000/players/')
  players.value = await res.json()
}

onMounted(fetchPlayers)
</script>

<style scoped>
.players-page {
  padding: 2rem 1rem;
  max-width: 1200px;
  margin: 0 auto;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}
.players-title {
  font-size: 2rem;
  font-weight: 600;
  color: #111827;
  margin-bottom: 1.5rem;
  text-align: center;
}

.players-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 1.5rem;
}

.player-card {
  background: #ffffff;
  border-radius: 0.75rem;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0,0,0,0.05);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}
.player-card:hover {
  transform: translateY(-6px);
  box-shadow: 0 8px 24px rgba(0,0,0,0.1);
}

.player-link {
  text-decoration: none;
  color: inherit;
  display: flex;
  flex-direction: column;
  height: 100%;
}

.player-image-wrapper {
  padding-top: 100%; 
  position: relative;
  background: #f3f4f6;
}
.player-image {
  position: absolute;
  top: 50%;
  left: 50%;
  width: 70%;
  height: 70%;
  transform: translate(-50%, -50%);
  object-fit: cover;
  border-radius: 50%;
  border: 3px solid #ffffff;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.player-info {
  padding: 1rem;
  text-align: center;
  margin-top: auto;
}
.player-nickname {
  font-size: 1.125rem;
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 0.25rem;
}
.player-name {
  font-size: 0.95rem;
  color: #4b5563;
}

@media (max-width: 640px) {
  .players-page {
    padding: 1rem;
  }
  .players-title {
    font-size: 1.5rem;
  }
  .player-info {
    padding: 0.75rem;
  }
}
</style>
