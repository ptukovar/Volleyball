<template>
  <div class="home-page">
    <div v-if="loading" class="loading">Loading…</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <div v-else>
      <section class="leaderboard">
        <h2>🏆 Top 3 Players</h2>
        <ol class="leader-list">
          <li v-for="p in topPlayers" :key="p.id">
            <span class="rank">#{{ p.rank }}</span>
            <span class="nick">{{ p.nickname }}</span>
            <span class="stat">{{ parseFloat(p.stats.win_rate).toFixed(2) }}% win rate</span>
          </li>
        </ol>
      </section>

      <section class="recent-games">
        <h2>🎮 Last 5 Games</h2>
        <ul class="games-list">
          <li v-for="g in recentGames" :key="g.id">
            <span class="game-id">Game #{{ g.id }}</span>
            <span class="game-date">
              {{ new Date(g.date).toLocaleDateString('en-GB', {
                year: 'numeric', month: 'short', day: 'numeric'
              }) }}
            </span>
          </li>
        </ul>
      </section>

      <section class="highlights">
        <div class="highlight-card">
          <h3>🏅 Top MVP</h3>
          <p class="highlight-name">
            {{ topMVP.first_name }} {{ topMVP.last_name }}
          </p>
          <p class="highlight-stat">
            {{ topMVP.stats.mvp_count }} MVP awards
          </p>
        </div>
        <div class="highlight-card">
          <h3>🎭 Biggest Impostor</h3>
          <p class="highlight-name">
            {{ biggestImpostor.first_name }} {{ biggestImpostor.last_name }}
          </p>
          <p class="highlight-stat">
            {{ biggestImpostor.stats.impostor_count }} impostor roles
          </p>
        </div>
      </section>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'

const players      = ref([])
const games        = ref([])
const fullPlayers  = ref([])
const error        = ref(null)
const loading      = ref(true)

onMounted(async () => {
  try {
    const pRes = await fetch('http://localhost:8000/players/')
    players.value = await pRes.json()

    fullPlayers.value = await Promise.all(
      players.value.map(async p => {
        const sRes = await fetch(`http://localhost:8000/players/${p.id}/stats/`)
        const stats = await sRes.json()
        return { ...p, stats }
      })
    )

    const gRes = await fetch('http://localhost:8000/games/')
    games.value = await gRes.json()

  } catch (e) {
    error.value = e.message
    console.error(e)
  } finally {
    loading.value = false
  }
})

const topPlayers = computed(() => {
  if (!fullPlayers.value.length) return []
  return fullPlayers.value
    .slice()
    .sort((a, b) => parseFloat(b.stats.win_rate) - parseFloat(a.stats.win_rate))
    .slice(0, 3)
    .map((p, i) => ({ ...p, rank: i + 1 }))
})

const recentGames = computed(() => {
  if (!games.value.length) return []
  return games.value
    .slice()
    .sort((a, b) => new Date(b.date) - new Date(a.date))
    .slice(0, 5)
})

const biggestImpostor = computed(() => {
  if (!fullPlayers.value.length) {
    return { first_name: '-', last_name: '', stats: { impostor_count: 0 } }
  }
  const max = fullPlayers.value.reduce((prev, curr) =>
    curr.stats.impostor_count > prev.stats.impostor_count ? curr : prev
  , fullPlayers.value[0])
  return max
})

const topMVP = computed(() => {
  if (!fullPlayers.value.length) {
    return { first_name: '-', last_name: '', stats: { mvp_count: 0 } }
  }
  const max = fullPlayers.value.reduce((prev, curr) =>
    curr.stats.mvp_count > prev.stats.mvp_count ? curr : prev
  , fullPlayers.value[0])
  return max
})
</script>


<style scoped>
.home-page {
  max-width: 1000px;
  margin: 2rem auto;
  padding: 1rem 2rem;
  background: #ffffff;
  border-radius: 0.75rem;
  box-shadow: 0 4px 16px rgba(0,0,0,0.05);
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  color: #1f2937;
}

.page-title {
  text-align: center;
  font-size: 2rem;
  margin-bottom: 2rem;
  font-weight: 600;
  color: #111827;
}

.leaderboard {
  margin-bottom: 2.5rem;
}
.leaderboard h2 {
  font-size: 1.5rem;
  margin-bottom: 1rem;
  color: #111827;
}
.leader-list {
  list-style: none;
  padding: 0;
}
.leader-list li {
  display: flex;
  align-items: center;
  background: #f9fafb;
  padding: 0.75rem 1rem;
  margin-bottom: 0.75rem;
  border-radius: 0.5rem;
  box-shadow: 0 2px 8px rgba(0,0,0,0.05);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.leader-list li:hover {
  transform: translateY(-3px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}
.rank {
  font-weight: 700;
  margin-right: 1rem;
  color: #3b82f6;
}
.nick {
  flex: 1;
  font-size: 1.125rem;
  font-weight: 500;
}
.stat {
  font-size: 0.95rem;
  color: #4b5563;
}

.recent-games {
  margin-bottom: 2.5rem;
}
.recent-games h2 {
  font-size: 1.5rem;
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
.games-list li {
  background: #f9fafb;
  padding: 0.75rem 1rem;
  border-radius: 0.5rem;
  box-shadow: 0 2px 8px rgba(0,0,0,0.05);
  display: flex;
  justify-content: space-between;
  align-items: center;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.games-list li:hover {
  transform: translateY(-3px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}
.game-id {
  font-weight: 600;
  color: #1f2937;
}
.game-date {
  font-size: 0.9rem;
  color: #6b7280;
}

.highlights {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 1.5rem;
}
.highlight-card {
  background: #f9fafb;
  padding: 1rem 1.25rem;
  border-radius: 0.5rem;
  box-shadow: 0 2px 8px rgba(0,0,0,0.05);
  text-align: center;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.highlight-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}
.highlight-card h3 {
  font-size: 1.25rem;
  margin-bottom: 0.5rem;
  color: #111827;
}
.highlight-name {
  font-size: 1.125rem;
  font-weight: 600;
  margin-bottom: 0.25rem;
  color: #1f2937;
}
.highlight-stat {
  font-size: 0.95rem;
  color: #4b5563;
}

.loading,
.error {
  text-align: center;
  font-size: 1.125rem;
  color: #6b7280;
  margin: 2rem 0;
}

@media (max-width: 768px) {
  .home-page {
    padding: 1rem;
  }
  .leader-list li,
  .games-list li,
  .highlight-card {
    padding: 0.6rem 0.8rem;
  }
  .page-title {
    font-size: 1.75rem;
  }
  .leaderboard h2,
  .recent-games h2 {
    font-size: 1.25rem;
  }
}
</style>
