const API = 'http://localhost:5001';


// -------- JOGOS --------


function carregarJogos() {
fetch(`${API}/boardgame`)
.then(res => res.json())
.then(data => {
const lista = document.getElementById('listaJogos');
lista.innerHTML = '';
data.jogos.forEach(j => {
const li = document.createElement('li');
li.innerHTML = `#${j.id_jogo} - ${j.nome_jogo}
<button onclick="deletarJogo(${j.id_jogo})">Excluir</button>`;
lista.appendChild(li);
});
});
}


function criarJogo() {
fetch(`${API}/boardgame`, {
method: 'POST',
headers: { 'Content-Type': 'application/json' },
body: JSON.stringify({
nome_jogo: document.getElementById('nomeJogo').value,
editora: document.getElementById('editoraJogo').value,
avaliacao: document.getElementById('avaliacaoJogo').value || null,
data_aquisicao: document.getElementById('dataJogo').value
})
}).then(carregarJogos);
}


function deletarJogo(id) {
fetch(`${API}/boardgame?id_jogo=${id}`, { method: 'DELETE' })
.then(carregarJogos);
}


// -------- EXPANSÕES --------


function carregarExpansoes() {
fetch(`${API}/expansao`)
.then(res => res.json())
.then(data => {
const lista = document.getElementById('listaExpansoes');
lista.innerHTML = '';
data.expansoes.forEach(e => {
const li = document.createElement('li');
li.innerHTML = `#${e.id_expansao} - ${e.nome_expansao}
<button onclick="deletarExpansao(${e.id_expansao})">Excluir</button>`;
lista.appendChild(li);
});
});
}


function criarExpansao() {
fetch(`${API}/expansao`, {
method: 'POST',
headers: { 'Content-Type': 'application/json' },
body: JSON.stringify({
nome_expansao: document.getElementById('nomeExp').value,
id_jogo: document.getElementById('idJogoExp').value || null,
avaliacao: document.getElementById('avaliacaoExp').value || null,
data_aquisicao: document.getElementById('dataExp').value
})
}).then(carregarExpansoes);
}


function deletarExpansao(id) {
fetch(`${API}/expansao?id_expansao=${id}`, { method: 'DELETE' })
.then(carregarExpansoes);
}


// Inicialização
carregarJogos();
carregarExpansoes();