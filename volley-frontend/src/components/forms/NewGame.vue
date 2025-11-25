<template>
  <div class="new-game">
    <h2>Create New Game</h2>
    <label>
      Date and Time:
      <input type="datetime-local" v-model="gameDate" />
    </label>
    <label>
      Number of sets:
      <select v-model="sets">
        <option value="1">1</option>
        <option value="2">2</option>
        <option value="3">3</option>
      </select>
    </label>

    <div v-for="i in parseInt(sets)" :key="i" class="set-row">
      <div class="set-label">Set {{ i }}:</div>
      <input type="number" v-model="scores[i-1].team1" min="0" placeholder="Team 1" />
      <input type="number" v-model="scores[i-1].team2" min="0" placeholder="Team 2" />
    </div>

    <div class="draft">
      <h3>Player Assignment</h3>
      <div class="columns">
        <div class="col" @dragover.prevent @dragenter.prevent @drop="drop('available')">
          <h4>Available Players</h4>
          <ul>
            <li v-for="p in available" :key="p.id" draggable="true"
                @dragstart="dragStart($event, p, 'available')">
              {{ p.first_name }} {{ p.last_name }}
            </li>
          </ul>
        </div>
        <div class="col" @dragover.prevent @dragenter.prevent @drop="drop('team1')">
          <h4>Team 1</h4>
          <ul>
            <li v-for="p in team1" :key="p.id" draggable="true"
                @dragstart="dragStart($event, p, 'team1')">
              {{ p.first_name }} {{ p.last_name }}
            </li>
          </ul>
        </div>
        <div class="col" @dragover.prevent @dragenter.prevent @drop="drop('team2')">
          <h4>Team 2</h4>
          <ul>
            <li v-for="p in team2" :key="p.id" draggable="true"
                @dragstart="dragStart($event, p, 'team2')">
              {{ p.first_name }} {{ p.last_name }}
            </li>
          </ul>
        </div>
      </div>

      <label>
        MVP:
        <select v-model="mvp">
          <option v-for="p in allAssigned" :key="p.id" :value="p.id">
            {{ p.first_name }} {{ p.last_name }}
          </option>
        </select>
      </label>
      <label>
        Impostor:
        <select v-model="impostor">
          <option v-for="p in allAssigned" :key="p.id" :value="p.id">
            {{ p.first_name }} {{ p.last_name }}
          </option>
        </select>
      </label>
    </div>

    <button class="submit-button" @click="submitAll" :disabled="submitting">
      {{ submitting ? 'Processing...' : 'Create Game and Save All' }}
    </button>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'

const gameDate = ref('')
const sets = ref('1')
const scores = ref([
  { team1: 0, team2: 0 },
  { team1: 0, team2: 0 },
  { team1: 0, team2: 0 }
])
const available = ref([])
const team1 = ref([])
const team2 = ref([])
const mvp = ref(null)
const impostor = ref(null)
const router = useRouter()

const allAssigned = computed(() => [...team1.value, ...team2.value])
const submitting = ref(false)
let dragData = null

onMounted(async () => {
  const res = await fetch('http://localhost:8000/players/')
  available.value = await res.json()
})

function dragStart(event, player, from) {
  dragData = { player, from }
  event.dataTransfer.effectAllowed = 'move'
}

function drop(to) {
  if (!dragData) return
  const { player, from } = dragData

  if (from === 'available') available.value = available.value.filter(p => p.id !== player.id)
  if (from === 'team1') team1.value = team1.value.filter(p => p.id !== player.id)
  if (from === 'team2') team2.value = team2.value.filter(p => p.id !== player.id)

  if (to === 'available') available.value.push(player)
  if (to === 'team1') team1.value.push(player)
  if (to === 'team2') team2.value.push(player)
  dragData = null
}

async function submitAll() {
  if (allAssigned.value.length === 0) {
    alert('Assign players to teams first!')
    return
  }
  submitting.value = true
  try {
    const resGame = await fetch('http://localhost:8000/games/', {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ date: gameDate.value })
    })
    const { id: gameId } = await resGame.json()
    for (const p of team1.value) {
      await fetch(`http://localhost:8000/games/${gameId}/players-add/`, {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ player_id: p.id, team: 1 })
      })
    }
    for (const p of team2.value) {
      await fetch(`http://localhost:8000/games/${gameId}/players-add/`, {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ player_id: p.id, team: 2 })
      })
    }
    const count = parseInt(sets.value)
    for (let i = 0; i < count; i++) {
      const sc = scores.value[i]
      await fetch(`http://localhost:8000/games/${gameId}/sets/`, {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ set_number: i+1, team1_score: sc.team1, team2_score: sc.team2 })
      })
    }
    const wins1 = scores.value.slice(0, count).filter(s => s.team1 > s.team2).length
    const wins2 = scores.value.slice(0, count).filter(s => s.team2 > s.team1).length
    await fetch(`http://localhost:8000/games/${gameId}/results/`, {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ sets_team1: wins1, sets_team2: wins2, mvp: mvp.value, impostor: impostor.value })
    })
    router.push('/games')
  } catch (e) {
    console.error(e)
    alert('Error: ' + e.message)
  } finally {
    submitting.value = false
  }
}
</script>

<style scoped>
.new-game {
  max-width: 800px;
  margin: 2rem auto;
  padding: 2rem;
  background: #ffffff;
  border-radius: 0.75rem;
  box-shadow: 0 4px 16px rgba(0,0,0,0.05);
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  color: #1f2937;
}
.new-game h2 {
  text-align: center;
  font-size: 1.75rem;
  margin-bottom: 1.5rem;
}
.new-game label {
  display: block;
  font-weight: 500;
  color: #374151;
  margin-bottom: 1rem;
}
.new-game input,
.new-game select {
  width: 100%;
  max-width: 320px;
  padding: 0.5rem 0.75rem;
  border: 1px solid #d1d5db;
  border-radius: 0.375rem;
  font-size: 1rem;
  margin-bottom: 1rem;
  transition: border-color 0.2s, box-shadow 0.2s;
}
.set-row {
  display: flex;
  align-items: center;
  margin-bottom: 1rem;
}
.set-label {
  font-weight: 600;
  margin-right: 1rem;
}
.draft {
  margin-top: 2rem;
}
.columns {
  display: flex;
  gap: 1rem;
  margin-bottom: 1rem;
}
.col {
  flex: 1;
  background: #f9fafb;
  border: 1px solid #e5e7eb;
  border-radius: 0.5rem;
  padding: 1rem;
  min-height: 150px;
}
.col h4 {
  margin-bottom: 0.5rem;
  font-size: 1.125rem;
}
.col ul {
  list-style: none;
  padding: 0;
}
.col li {
  padding: 0.5rem;
  margin-bottom: 0.5rem;
  background: #ffffff;
  border: 1px solid #d1d5db;
  border-radius: 0.375rem;
  cursor: grab;
  transition: background-color 0.2s;
}
.col li:hover {
  background: #f3f4f6;
}
.submit-button {
  display: block;
  width: 100%;
  padding: 0.75rem;
  background-color: #3b82f6;
  color: #ffffff;
  font-size: 1rem;
  font-weight: 600;
  border: none;
  border-radius: 0.375rem;
  cursor: pointer;
  transition: background-color 0.3s;
}
.submit-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
</style>

