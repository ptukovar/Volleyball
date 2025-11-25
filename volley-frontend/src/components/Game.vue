<template>
  <div class="game-card">
    <div v-if="loading" class="loading">Loading…</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <div v-else>
      <header class="card-header">
        <h2>Game #{{ game.id }}</h2>
        <div class="meta">
          <span>{{ new Date(game.date).toLocaleDateString() }}</span>
          <span>{{ new Date(game.date).toLocaleTimeString() }}</span>
        </div>
      </header>

      <section class="card-body">
        <div class="result-row">
          <div>
            <strong>MVP: </strong>
            <span v-if="gameResults?.mvp && gameResults.mvp !== 'N/A'">{{ gameResults.mvp }}</span>
            <span v-else>—</span>
          </div>
          <div>
            <strong>Impostor: </strong>
            <span v-if="gameResults?.impostor && gameResults.impostor !== 'N/A'">{{ gameResults.impostor }}</span>
            <span v-else>—</span>
          </div>
        </div>

        <div class="teams">
          <div class="team">
            <h3>Team 1</h3>
            <ul v-if="team1.length">
              <li v-for="p in team1" :key="p.id">
                {{ p.first_name }} {{ p.last_name }}
              </li>
            </ul>
            <p v-else>No players</p>
          </div>
          <div class="team">
            <h3>Team 2</h3>
            <ul v-if="team2.length">
              <li v-for="p in team2" :key="p.id">
                {{ p.first_name }} {{ p.last_name }}
              </li>
            </ul>
            <p v-else>No players</p>
          </div>
        </div>

        <div class="sets">
          <h3>Sets</h3>
          <ul v-if="game.sets?.length">
            <li v-for="s in game.sets" :key="s.id">
              Set {{ s.set_number }}: {{ s.team1_score }} – {{ s.team2_score }}
            </li>
          </ul>
          <p v-else>No sets recorded</p>
        </div>
      </section>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'

const route   = useRoute()
const game    = ref({})
const loading = ref(true)
const error   = ref(null)
const mvp = ref(null)
const impostor = ref(null)
const gameResults = ref(null)

const team1 = ref([])
const team2 = ref([])

async function fetchGameData() {
  try {
    loading.value = true
    error.value   = null

    const resGame = await fetch(`http://localhost:8000/games/${route.params.id}/`)
    if (!resGame.ok) throw new Error('Failed to fetch game')
    game.value = await resGame.json()
    const resMap = await fetch(`http://localhost:8000/games/${route.params.id}/players/`)
    if (!resMap.ok) throw new Error('Failed to fetch player mappings')
    const mappings = await resMap.json() 

    const detailed = await Promise.all(
      mappings.map(async m => {
        const r = await fetch(`http://localhost:8000/players/${m.player_id}/`)
        if (!r.ok) throw new Error(`Failed to fetch player ${m.player_id}`)
        const p = await r.json()
        return { ...p, team: m.team }
      })
    )

    team1.value = detailed.filter(p => p.team === 1)
    team2.value = detailed.filter(p => p.team === 2)

    const resSets = await fetch(`http://localhost:8000/games/${route.params.id}/sets/`)
    if (!resSets.ok) throw new Error('Failed to fetch sets')
    game.value.sets = await resSets.json()
    
    const gameRes = await fetch(`http://localhost:8000/games/${route.params.id}/results/`)
    if (!gameRes.ok) throw new Error('Failed to fetch game results')
    gameResults.value = await gameRes.json()
    mvp.value = gameResults.value.mvp ? await fetch(`http://localhost:8000/players/${gameResults.value.mvp}/`)
      .then(res => res.ok ? res.json() : null) : null
    impostor.value = gameResults.value.impostor ? await fetch(`http://localhost:8000/players/${gameResults.value.impostor}/`)
      .then(res => res.ok ? res.json() : null) : null
    console.log('mvp', mvp.value)
    console.log('impostor', impostor.value)
    if (mvp.value !== null && mvp.value.first_name) {
      gameResults.value.mvp = `${mvp.value.first_name} ${mvp.value.last_name}`
    } else {
      gameResults.value.mvp = 'N/A'
    }

    if (impostor.value !== null && impostor.value.first_name) {
      gameResults.value.impostor = `${impostor.value.first_name} ${impostor.value.last_name}`
    } else {
      gameResults.value.impostor = 'N/A'
    }
  } catch (e) {
    error.value = e.message
    console.error(e)
  } finally {
    loading.value = false
  }
}

onMounted(fetchGameData)
</script>

<style scoped>
.game-card {
  max-width: 800px;
  margin: 2rem auto;
  border-radius: 0.75rem;
  box-shadow: 0 4px 16px rgba(0,0,0,0.05);
  overflow: hidden;
  font-family: 'Segoe UI', Tahoma, Verdana, sans-serif;
}

.card-header {
  background: var(--color-primary, #3b82f6);
  color: white;
  padding: 1.5rem;
  text-align: center;
}
.card-header h2 {
  margin: 0;
  font-size: 2rem;
}
.card-header .meta {
  margin-top: 0.5rem;
  font-size: 0.9rem;
  opacity: 0.8;
}

.card-body {
  background: white;
  padding: 2rem;
}

.loading, .error {
  text-align: center;
  padding: 2rem;
  font-size: 1.125rem;
  color: var(--color-muted, #6b7280);
}

.result-row {
  display: flex;
  justify-content: space-between;
  margin-bottom: 1.5rem;
}
.result-row div {
  font-size: 1rem;
}

.teams {
  display: flex;
  gap: 2rem;
  margin-bottom: 1.5rem;
}
.team {
  flex: 1;
  background: var(--color-alt-bg, #f9fafb);
  border-radius: 0.5rem;
  padding: 1rem;
  box-shadow: 0 2px 8px rgba(0,0,0,0.03);
}
.team h3 {
  margin-top: 0;
  font-size: 1.25rem;
  margin-bottom: 0.75rem;
  border-bottom: 1px solid var(--color-border, #e5e7eb);
}
.team ul {
  list-style: none;
  padding: 0;
  margin: 0;
}
.team li {
  padding-left: 0.5rem;
  margin: 0.5rem 0;
  position: relative;
}
.team li::before {
  content: '•';
  position: absolute;
  left: 0;
  color: var(--color-primary, #3b82f6);
}

.sets {
  margin-top: 2rem;
}
.sets h3 {
  font-size: 1.5rem;
  margin-bottom: 0.75rem;
}
.sets ul {
  list-style: none;
  padding: 0;
  margin: 0;
  background: var(--color-alt-bg, #f9fafb);
  border-radius: 0.5rem;
  box-shadow: 0 2px 8px rgba(0,0,0,0.03);
}
.sets li {
  display: flex;
  justify-content: space-between;
  padding: 0.75rem 1rem;
  border-bottom: 1px solid var(--color-border, #e5e7eb);
}
.sets li:last-child {
  border-bottom: none;
}
</style>
