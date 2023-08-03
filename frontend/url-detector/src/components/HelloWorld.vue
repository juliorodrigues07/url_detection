<template>

  <div class="container">
    <div class="jumbotron vertical-center">
    
      <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootswatch@4.5.2/dist/lux/bootstrap.min.css" 
      integrity="sha384-9+PGKSqjRdkeAU7Eu4nkJU8RFaH8ace8HGXnkiKMP9I9Te0GJ4/km3L1Z8tXigpG" crossorigin="anonymous">
      
      <div class="row">
        <div class="col-sm-12">
          <h2 class="text-center bg-primary text-white">URL Detector</h2>
          <hr>
          
          <b-form @submit="onSubmit" class="w-50 text-center">
					
            <b-form-group class="input-form-control" id="form-url-group" label="URL" label-for="form-url-input">
              
              <b-form-input id="form-url-input" 
                    type="text" 
                    v-model="detectionForm.URL" 
                    required 
                    placeholder="Enter the URL...">
              </b-form-input>

              <span class="exclamation">
                <font-awesome-icon icon="fas fa-exclamation-circle" style="height: 20px;"></font-awesome-icon>
              </span>

              <span class="check">
                <font-awesome-icon icon="fas fa-check-circle" style="height: 20px;"></font-awesome-icon>
              </span>

              <b-small></b-small>
            </b-form-group>

            <b-form-group class="input-form-control" id="form-algorithm-group" label="Algorithm" label-for="form-algorithm-input">
              
              <select v-model="selected" required>
                <option disabled value="">Select an algorithm</option>
                <option>Logistic Regression</option>
                <option>XGBoost</option>
              </select>

            </b-form-group>

					<b-button class="sub-but" type="submit" variant="btn btn-success">Classify</b-button>

				</b-form>

        <br><br>
        
        <table class="table table-hover">
          <thead>
            <tr>
              <th scope="col">URL</th>
              <th scope="col">Classified as</th>
              <th scope="col">Reliability</th>
              <th scope="col">Algorithm</th>
            </tr>
          </thead>
          <!-- <tbody v-for="detection, index in detections" :key="index">
            <tr>
              <td>{{ detection.URL }}</td>
              <td>{{ detection.Type }}</td>
              <td>{{ detection.Probability }}</td>
              <td>{{ detection.Algorithm }}</td>
            </tr>
          </tbody> -->
        </table>

        <footer class="bg-primary text-white text-center" style="border-radius: 10px;">
          Copyright &copy;. All Rights Reserved 2023.
        </footer>

				</div>
			</div>
    </div>
  </div>

</template>

<script>

  import axios from "axios";

  export default {
    name: "HelloWorld",

    data() {
      return {
        selected: 'Select an algorithm',
        detections: [],
        detectionForm: 
        {
          'URL': ''
        },
        msg: "Not working",
      };
    },

    methods: {

      getDetections() {
        const path = "http://localhost:5000";
        axios
          .get(path)
          .then((res) => {
            console.log(res.data);
            this.msg = res.data;
          })

          .catch((err) => {
            console.error(err);
          });
      },

      clearForm() 
      {
        this.detectionForm.URL = '';
        this.selected = 'Select an algorithm';
      },

      checkInputs() {
        
        let validURL = false;
        let urlInput = document.getElementById('form-url-input');
        
        try { 
          validURL = Boolean(new URL(this.detectionForm.URL));
        } catch(e) { 
          validURL = false;
        }

        if (validURL)
          this.setSuccessFor(urlInput);
        else 
          this.setErrorFor(urlInput, 'Invalid URL.');

        const formControls = document.querySelectorAll('.input-form-control');
        
        const formIsValid = [...formControls].every(formControl => {
          return (formControl.className != 'input-form-control error');
        });

        return formIsValid;
      },

      setSuccessFor(field) {

        let formControl = field.parentElement;
        formControl.className = 'input-form-control success';

        setTimeout(function() {
          formControl.className = 'input-form-control';
        }, 2500);
      },

      setErrorFor(field, message) {

        let formControl = field.parentElement;
        let small = formControl.querySelector('b-small');

        formControl.className = 'input-form-control error';
        small.innerText = message;
      },

      onSubmit(e) {
        e.preventDefault();
        let check = this.checkInputs();

        if (check) {

          const payload = {
            Name: this.detectionForm.URL,
            Algorithm: this.selected
          };

          this.classifyURL(payload);
        }

        this.clearForm();
      },
    },
    
    created() {
      this.getDetections();
    },
  };

</script>

<style scoped>

  h2 {
    padding: 15px;
    border-radius: 10px;
  }

  .jumbotron {
    position: absolute;
    width: 90%;
    left: 5%;
  }

  .input-form-control {
    margin: 0 auto;
    color: #ffffff;
  }

  .w-50 {
    margin: 0 auto;
    padding: 20px;
    border-radius: 20px;
    background-color: #201c1c;  
    font-size: x-large;
  }

  .sub-but {
    font-size: large;
    border-radius: 5px;
    margin-top: 30px;
  }

  #form-url-input {
    margin: 0 auto;
    border-radius: 5px;
    width: 90%;
  }

  select {
    padding: 10px;
  }

  .input-form-control .exclamation {
    visibility: hidden;
  }

  .input-form-control.error .exclamation {
    color: #ff0000;
    position: relative;
    bottom: 38px;
    left: 49%;
    visibility: visible;
  }

  .input-form-control .check {
    visibility: hidden;
  }

  .input-form-control.success .check {
    color: #73ff00;
    position: relative;
    bottom: 40px;
    left: 40%;
    visibility: visible;
  }

  .input-form-control.success input {
    border: 4px solid #73ff00;
  }

  .input-form-control.error input {
    border: 4px solid #ff0000;
  }

  .input-form-control b-small {
    font-size: 14px;
    position: relative;
    right: 40%;
    margin-top: 5px;
    visibility: hidden;
  }

  .input-form-control.error b-small {
    color: #ff0000;
    visibility: visible;
  }
</style>
