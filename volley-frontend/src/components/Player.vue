<template>
  <div class="player" v-if="player">
    <h2>Player info</h2>
    <div class="player-details">
      <img :src="player.image" alt="Player Image" width="100" height="100" />
      <p><strong>First Name:</strong> {{ player.first_name }}</p>
      <p><strong>Last Name:</strong> {{ player.last_name }}</p>
      <p><strong>Nickname:</strong> {{ player.nickname }}</p>
      <p><strong>Role:</strong> {{ player.role === 0 ? 'Player' : 'Admin' }}</p>
    </div>
    <h3>Player statistics</h3>
    <div class="player-stats">
      <p><strong>Total Games:</strong> {{ stats.total_games}}</p>
      <p><strong>Wins:</strong> {{ stats.wins }}</p>
      <p><strong>Losses:</strong> {{ stats.losses }}</p>
      <p><strong>Win Rate:</strong> {{ parseFloat(stats.win_rate).toFixed(2) }}%</p>
      <p><strong>Wins Team 1:</strong> {{ stats.wins_team1 }}</p>
      <p><strong>Wins Team 2:</strong> {{ stats.wins_team2 }}</p>
      <p><strong>Total Sets:</strong> {{ stats.total_sets }}</p>
      <p><strong>Sets Won:</strong> {{ stats.sets_won }}</p>
      <p><strong>Sets Lost:</strong> {{ stats.sets_lost }}</p>
      <p><strong>Sets Win Rate:</strong> {{ parseFloat(stats.sets_win_rate).toFixed(2) }}%</p>
      <p><strong>Average winning points:</strong> {{ parseFloat(stats.avg_winning_points).toFixed(1) }}</p>
      <p><strong>Average losing points:</strong> {{ parseFloat(stats.avg_losing_points).toFixed(1) }}</p>
      <p><strong>Average points:</strong> {{ parseFloat(stats.avg_points).toFixed(1) }}</p>
      <p><strong>MVP Count:</strong> {{ stats.mvp_count }}</p>
      <p><strong>Impostor Count:</strong> {{ stats.impostor_count }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'

const route    = useRoute()
const playerId = route.params.id
const player   = ref(null)
const stats  = ref(null)

onMounted(async () => {
  const res = await fetch(`http://localhost:8000/players/${playerId}`, {
    headers: { 'Content-Type': 'application/json' }
  })
  if (!res.ok) {
    console.error('Chyba při načítání hráče:', res.status)
    return
  }
  const resStats = await fetch(`http://localhost:8000/players/${playerId}/stats/`, {
    headers: { 'Content-Type': 'application/json' }
  })
  stats.value = await resStats.json()
  console.log(stats.value)
  player.value = await res.json()
})
</script>

<style scoped>
.player {
  max-width: 800px;
  margin: 2rem auto;
  padding: 2rem;
  background-color: #ffffff;
  border-radius: 0.75rem;
  box-shadow: 0 4px 16px rgba(0,0,0,0.05);
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  color: #1f2937;
}

.player h2,
.player h3 {
  margin-bottom: 1rem;
  font-weight: 600;
}
.player h2 {
  font-size: 1.75rem;
  text-align: center;
}
.player h3 {
  font-size: 1.25rem;
  border-bottom: 2px solid #e5e7eb;
  padding-bottom: 0.5rem;
  margin-top: 2rem;
}

.player-details,
.player-stats {
  background-color: #f9fafb;
  border-radius: 0.5rem;
  padding: 1.5rem;
  margin-bottom: 1.5rem;
}

.player-details {
  display: grid;
  grid-template-columns: 1fr 1fr;
  row-gap: 0.75rem;
  column-gap: 1.5rem;
}
.player-details p {
  margin: 0;
  font-size: 1rem;
  line-height: 1.4;
}
.player-details strong {
  color: #374151;
}

.player-details img {
  grid-column: 1 / -1;
  display: block;
  margin: 0.5rem auto 0;
  width: 160px;
  height: 160px;
  object-fit: cover;
  border-radius: 50%;
  border: 3px solid #ffffff;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.player-stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 1rem;
}
.player-stats p {
  margin: 0;
  font-size: 0.95rem;
}
.player-stats strong {
  display: block;
  font-weight: 600;
  margin-bottom: 0.25rem;
  color: #374151;
}

@media (max-width: 600px) {
  .player {
    padding: 1.5rem;
  }
  .player-details {
    grid-template-columns: 1fr;
  }
  .player-details img {
    width: 100px;
    height: 100px;
  }
  .player h2 {
    font-size: 1.5rem;
  }
  .player h3 {
    font-size: 1.125rem;
  }
}
</style>
