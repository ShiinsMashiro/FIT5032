<template>
  <div class="container mt-5">
    <div class="row">
      <div class="col-md-8 offset-md-2">
        <h1 class="text-center">User Information Form</h1>
        <form @submit.prevent="submitForm">
          <div class="row mb-3">
            <div class="col-md-6 col-sm-6">
              <label for="username" class="form-label">Username</label>
              <input
                type="text"
                class="form-control"
                id="username"
                @blur="() => validateName(true)"
                @input="() => validateName(false)"
                v-model="formData.username"
              />
              <div v-if="errors.username" class="text-danger">{{ errors.username }}</div>
            </div>
            <div class="col-md-6 col-sm-6">
              <label for="password" class="form-label">Password</label>
              <input
                type="password"
                class="form-control"
                id="password"
                @blur="() => validatePassword(true)"
                @input="() => validatePassword(false)"
                v-model="formData.password"
              />
              <div v-if="errors.password" class="text-danger">{{ errors.password }}</div>
            </div>
          </div>
          <div class="row mb-3">
            <div class="col-md-6 col-sm-6">
              <div class="form-check">
                <input
                  type="checkbox"
                  class="form-check-input"
                  id="isAustralian"
                  @change="() => validateResident(true)"
                  v-model="formData.isAustralian"
                />
                <label class="form-check-label" for="isAustralian">Australian Resident?</label>
              </div>
              <div v-if="errors.resident" class="text-danger">{{ errors.resident }}</div>
            </div>
            <div class="col-md-6 col-sm-6">
              <label for="gender" class="form-label">Gender</label>
              <select
                class="form-select"
                id="gender"
                @change="() => validateGender(true)"
                v-model="formData.gender"
              >
                <option value="" disabled selected>Select gender</option>
                <option value="male">Male</option>
                <option value="female">Female</option>
                <option value="other">Other</option>
              </select>
              <div v-if="errors.gender" class="text-danger">{{ errors.gender }}</div>
            </div>
          </div>
          <div class="mb-3">
            <label for="reason" class="form-label">Reason for joining</label>
            <textarea
              class="form-control"
              id="reason"
              rows="3"
              @blur="() => validateReason(true)"
              @input="() => validateReason(false)"
              v-model="formData.reason"
            ></textarea>
            <div v-if="errors.reason" class="text-danger">{{ errors.reason }}</div>
          </div>
          <div class="text-center">
            <button type="submit" class="btn btn-primary me-2">Submit</button>
            <button type="button" class="btn btn-secondary" @click="clearForm">Clear</button>
          </div>
        </form>
      </div>
    </div>

    <!-- PrimeVue DataTable for Submitted Users -->
    <div class="row mt-5" v-if="submittedCards.length">
      <div class="col-12">
        <DataTable :value="submittedCards" tableStyle="min-width: 50rem" class="p-datatable-sm custom-datatable">
          <Column field="username" header="Username"></Column>
          <Column field="password" header="Password"></Column>
          <Column field="isAustralian" header="Australian Resident"></Column>
          <Column field="gender" header="Gender"></Column>
          <Column field="reason" header="Reason"></Column>
        </DataTable>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'

const formData = ref({
  username: '',
  password: '',
  isAustralian: false,
  reason: '',
  gender: ''
})

const submittedCards = ref([])

const submitForm = () => {
  validateName(true);
  validatePassword(true);
  validateResident(true);
  validateGender(true);
  validateReason(true);
  if (!errors.value.username && !errors.value.password && !errors.value.resident && !errors.value.gender && !errors.value.reason) {
    submittedCards.value.push({ ...formData.value });
    clearForm();
  }
};

const clearForm = () => {
  formData.value = {
    username: '',
    password: '',
    isAustralian: false,
    reason: '',
    gender: ''
  };
  errors.value = {
    username: null,
    password: null,
    resident: null,
    gender: null,
    reason: null
  };
};

const errors = ref({
  username: null,
  password: null,
  resident: null,
  gender: null,
  reason: null
})

const validateName = (blur) => {
  if (formData.value.username.length < 3) {
    if (blur) errors.value.username = "Name must be at least 3 characters";
  } else {
    errors.value.username = null;
  }
};

const validatePassword = (blur) => {
  const password = formData.value.password;
  const minLength = 8;
  const hasUppercase = /[A-Z]/.test(password);
  const hasLowercase = /[a-z]/.test(password);
  const hasNumber = /\d/.test(password);
  const hasSpecialChar = /[!@#$%^&*(),.?":{}|<>]/.test(password);

  if (password.length < minLength) {
    if (blur) errors.value.password = `Password must be at least ${minLength} characters long.`;
  } else if (!hasUppercase) {
    if (blur) errors.value.password = "Password must contain at least one uppercase letter.";
  } else if (!hasLowercase) {
    if (blur) errors.value.password = "Password must contain at least one lowercase letter.";
  } else if (!hasNumber) {
    if (blur) errors.value.password = "Password must contain at least one number.";
  } else if (!hasSpecialChar) {
    if (blur) errors.value.password = "Password must contain at least one special character.";
  } else {
    errors.value.password = null;
  }
};

const validateResident = (blur) => {
  if (!formData.value.isAustralian) {
    if (blur) errors.value.resident = "You must be an Australian resident.";
  } else {
    errors.value.resident = null;
  }
};

const validateGender = (blur) => {
  if (!formData.value.gender) {
    if (blur) errors.value.gender = "Gender is required.";
  } else {
    errors.value.gender = null;
  }
};

const validateReason = (blur) => {
  if (!formData.value.reason || formData.value.reason.trim().length < 10) {
    if (blur) errors.value.reason = "Reason must be at least 10 characters long.";
  } else {
    errors.value.reason = null;
  }
};
</script>

<style>
/* Exact light theme matching the slide */
.p-datatable.custom-datatable {
  background: #ffffff !important;
}
.p-datatable.custom-datatable .p-datatable-thead > tr > th {
  background-color: transparent !important;
  color: #212529 !important;
  font-weight: 600 !important;
  border: none !important;
  border-bottom: 1px solid #dee2e6 !important;
  padding: 12px 16px !important;
}
.p-datatable.custom-datatable .p-datatable-tbody > tr {
  background-color: transparent !important;
}
.p-datatable.custom-datatable .p-datatable-tbody > tr > td {
  border: none !important;
  border-bottom: 1px solid #f1f3f5 !important;
  color: #212529 !important;
  padding: 12px 16px !important;
}
/* Hide any commercial license banners if rendered */
div[style*="fixed"][style*="bottom"], 
div:has(> a[href*="primevue"]),
div:has(> [class*="license"]) {
  display: none !important;
}
</style>