<template>
  <div class="app-container">
    <header class="header">
      <h1 class="title">🔥 Sneaker Paradise 🔥</h1>
      <button @click="toggleAddTenisModal" class="btn-primary">
        + Añadir Sneaker
      </button>
    </header>

    <div v-if="activeAddTenisModal" class="form-modal">
      <form @submit.prevent="handleAddSubmit" class="form">
        <input v-model="addTenisForm.nombre" placeholder="Nombre" required />
        <input v-model.number="addTenisForm.precio" type="number" placeholder="Precio" required />
        <input v-model.number="addTenisForm.stock" type="number" placeholder="Stock" required />
        <div class="form-buttons">
          <button type="submit" class="btn-primary">Guardar Sneaker</button>
          <button type="button" @click="toggleAddTenisModal" class="btn-cancel">Cancelar</button>
        </div>
      </form>
    </div>
    <main>
      <div class="sneaker-grid">
        <div
          v-for="(tenisItem, index) in tenis"
          :key="tenisItem.id"
          class="card"
          :style="cardBackground(index)"
        >
          <div
            class="card-content"
            :class="{ 'special-font': index < 3 }"
          >
            <h2 class="card-title">{{ tenisItem.nombre }}</h2>
            <p class="card-price">${{ tenisItem.precio.toFixed(2) }}</p>
            <p class="card-stock">
              Stock: <strong>{{ tenisItem.stock }}</strong>
            </p>
            <p
              class="availability"
              :class="tenisItem.stock > 0 ? 'available' : 'unavailable'"
            >
              {{ tenisItem.stock > 0 ? "Disponible" : "Agotado" }}
            </p>
            <div class="btn-group">
              <button
                @click="increaseStock(index)"
                class="btn btn-increase"
                title="Aumentar stock"
              >
                +
              </button>
              <button
                @click="decreaseStock(index)"
                :disabled="tenisItem.stock === 0"
                class="btn btn-decrease"
                title="Disminuir stock"
              >
                -
              </button>
            </div>
          </div>
        </div>
      </div>
    </main>

    <transition name="fade">
      <div v-if="showMessage" class="alert-message">{{ message }}</div>
    </transition>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      tenis: [],
      addTenisForm: {
        nombre: "",
        precio: null,
        stock: null,
      },
      activeAddTenisModal: false,
      message: "",
      showMessage: false,
      cardColors: [
        ["#FF6B6B", "#FFD93D"],
        ["#6BCB77", "#4D96FF"],
        ["#FF6FD8", "#845EC2"],
        ["#00C9A7", "#92FE9D"],
        ["#F9F586", "#F29E4C"],
        ["#FF9671", "#FFC75F"],
        ["#D65DB1", "#845EC2"],
      ],
    };
  },
  methods: {
    toggleAddTenisModal() {
      this.activeAddTenisModal = !this.activeAddTenisModal;
      if (!this.activeAddTenisModal) this.handleAddReset();
    },
    async getTenis() {
      const query = `
        query {
          tenis {
            id
            nombre
            precio
            stock
            disponible
          }
        }
      `;
      try {
        const res = await axios.post("http://localhost:5001/graphql", { query });
        this.tenis = res.data.data.tenis;
      } catch (err) {
        console.error("Error al obtener tenis:", err);
      }
    },
    async updateStock(id, amount) {
      const mutation = `
        mutation {
          updateStock(id: "${id}", amount: ${amount}) {
            success
            message
            tenis {
              id
              stock
              disponible
            }
          }
        }
      `;
      try {
        await axios.post("http://localhost:5001/graphql", { query: mutation });
        this.getTenis();
      } catch (error) {
        console.error("Error al actualizar stock:", error);
      }
    },
    increaseStock(index) {
      const item = this.tenis[index];
      this.updateStock(item.id, 1);
    },
    decreaseStock(index) {
      const item = this.tenis[index];
      if (item.stock > 0) this.updateStock(item.id, -1);
    },
    async handleAddSubmit() {
      const { nombre, precio, stock } = this.addTenisForm;
      if (!nombre || precio === null || stock === null) {
        alert("Por favor llena todos los campos.");
        return;
      }

      const mutation = `
        mutation {
          addTenis(nombre: "${nombre}", precio: ${precio}, stock: ${stock}) {
            id
            nombre
            precio
            stock
            disponible
          }
        }
      `;
      try {
        const response = await axios.post("http://localhost:5001/graphql", {
          query: mutation,
        });
        if (response.data.errors) {
          alert("Error al agregar sneaker: " + response.data.errors[0].message);
          return;
        }

        this.message = `Sneaker "${nombre}" agregado con éxito!`;
        this.showMessage = true;

        await this.getTenis();
        this.toggleAddTenisModal();
        this.handleAddReset();

        setTimeout(() => (this.showMessage = false), 3000);
      } catch (error) {
        alert("Error al agregar sneaker.");
        console.error("Error:", error);
      }
    },
    handleAddReset() {
      this.addTenisForm = { nombre: "", precio: null, stock: null };
    },
    cardBackground(index) {
      const colors = this.cardColors[index % this.cardColors.length];
      return {
        background: `linear-gradient(135deg, ${colors[0]}, ${colors[1]})`,
        color: "white",
        boxShadow: `0 8px 20px ${colors[0]}99`,
      };
    },
  },
  created() {
    this.getTenis();
  },
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Pacifico&family=Roboto:wght@400;700&display=swap');

.app-container {
  max-width: 1100px;
  margin: 30px auto;
  font-family: "Roboto", sans-serif;
  padding: 0 20px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 40px;
}

.title {
  font-size: 2.8rem;
  color: #ff4757;
  text-shadow: 0 0 10px #ff6b81;
}

.btn-primary {
  background: linear-gradient(45deg, #ff6b6b, #ffd93d);
  border: none;
  color: white;
  padding: 14px 26px;
  font-size: 1.1rem;
  border-radius: 40px;
  box-shadow: 0 8px 20px #ff6b6bcc;
  cursor: pointer;
}

.form-modal {
  margin-bottom: 30px;
  padding: 20px;
  border: 2px dashed #ccc;
  border-radius: 12px;
  background-color: #fdfdfd;
}

.form input {
  display: block;
  width: 100%;
  padding: 10px;
  margin-bottom: 10px;
}

.form-buttons {
  display: flex;
  gap: 10px;
}

.btn-cancel {
  background-color: #aaa;
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 20px;
  cursor: pointer;
}

.sneaker-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 30px;
}

.card {
  border-radius: 20px;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  transition: transform 0.3s ease;
  min-height: 220px;
}

.card:hover {
  transform: translateY(-10px);
}

.card-content {
  display: flex;
  flex-direction: column;
  align-items: center; 
  justify-content: center; 
  text-align: center;
  flex-grow: 1;
  padding: 15px;
  font-family: "Roboto", sans-serif;
}

.special-font {
  font-family: 'Pacifico', cursive;
  font-weight: 700;
  font-size: 1.3rem;
  color: #fff;
}

.alert-message {
  background: #dff9fb;
  color: #130f40;
  padding: 15px;
  text-align: center;
  border-radius: 10px;
  margin-top: 20px;
  font-weight: 700;
  font-size: 1.2rem;
  box-shadow: 0 0 15px #c7ecee;
}

.card-title {
  font-weight: 900;
  font-size: 1.7rem;
  margin-bottom: 10px;
  text-shadow: 0 0 8px rgba(0,0,0,0.15);
}

.card-price {
  font-weight: 700;
  font-size: 1.3rem;
  margin-bottom: 10px;
}

.card-stock {
  font-weight: 500;
  font-size: 1.1rem;
  margin-bottom: 6px;
}

.availability {
  font-weight: 700;
  margin-bottom: 12px;
}

.available {
  color: #9AE66E;
  text-shadow: 0 0 5px #9AE66EBB;
}

.unavailable {
  color: #FF6B6B;
  text-shadow: 0 0 6px #FF6B6BBB;
}

.btn-group {
  display: flex;
  gap: 12px;
  justify-content: center;
}

.btn {
  font-size: 1.3rem;
  width: 45px;
  height: 45px;
  border-radius: 50%;
  border: none;
  cursor: pointer;
  font-weight: 900;
  color: white;
  box-shadow: 0 6px 18px #00000044;
  transition: background-color 0.3s ease;
}

.btn-increase {
  background-color: #6bcf77;
}

.btn-increase:hover {
  background-color: #52b254;
}

.btn-decrease {
  background-color: #ff6b6b;
}

.btn-decrease:hover:enabled {
  background-color: #c43c3c;
}

.btn-decrease:disabled {
  background-color: #ffb3b3;
  cursor: not-allowed;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s;
}
.fade-enter,
.fade-leave-to {
  opacity: 0;
}
</style>
