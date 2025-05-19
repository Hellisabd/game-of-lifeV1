
const canvas = document.getElementById("lifeCanvas");
const ctx = canvas.getContext("2d");

const cols = 52;
const rows = 7;
const cellSize = 20;
const width = cols * cellSize;
const height = rows * cellSize;
canvas.width = width;
canvas.height = height;

let grid = createGrid();
randomizeGrid(grid);

function createGrid() {
  return Array.from({ length: rows }, () => Array(cols).fill(0));
}

function randomizeGrid(grid) {
  for (let y = 0; y < rows; y++) {
    for (let x = 0; x < cols; x++) {
      grid[y][x] = Math.random() > 0.7 ? 1 : 0;
    }
  }
}

function getNextGeneration(grid) {
  const next = createGrid();

  for (let y = 0; y < rows; y++) {
    for (let x = 0; x < cols; x++) {
      const neighbors = countNeighbors(grid, x, y);
      const alive = grid[y][x];

      if (alive && (neighbors === 2 || neighbors === 3)) {
        next[y][x] = 1;
      } else if (!alive && neighbors === 3) {
        next[y][x] = 1;
      } else {
        next[y][x] = 0;
      }
    }
  }

  return next;
}

function countNeighbors(grid, x, y) {
  let sum = 0;
  for (let i = -1; i <= 1; i++) {
    for (let j = -1; j <= 1; j++) {
      const row = (y + i + rows) % rows;
      const col = (x + j + cols) % cols;
      sum += grid[row][col];
    }
  }
  sum -= grid[y][x];
  return sum;
}

function drawGrid(grid) {
  ctx.clearRect(0, 0, width, height);
  for (let y = 0; y < rows; y++) {
    for (let x = 0; x < cols; x++) {
      ctx.fillStyle = grid[y][x] ? "#26a641" : "#0d1117";
      ctx.fillRect(x * cellSize, y * cellSize, cellSize, cellSize);
    }
  }
}

function animate() {
  drawGrid(grid);
  grid = getNextGeneration(grid);
  setTimeout(animate, 1000);
}

animate();
