<template>

  <div class="container">
    <div class="jumbotron vertical-center">
    
      <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootswatch@4.5.2/dist/lux/bootstrap.min.css" 
      integrity="sha384-9+PGKSqjRdkeAU7Eu4nkJU8RFaH8ace8HGXnkiKMP9I9Te0GJ4/km3L1Z8tXigpG" crossorigin="anonymous">

      <!--Header-->
      <div class="row">
        <div class="col-sm-12">
          <h2 class="text-center bg-primary text-white">URL Detector</h2>
          <br>

          <!--Form for URL and associated classifying algorithm submission-->
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
                <option value="LR">Logistic Regression</option>
                <option value="XGB">XGBoost</option>
              </select>

            </b-form-group>

          <b-button class="sub-but" type="submit" variant="btn btn-success">Classify</b-button>

        </b-form>

        <br>
        <b-button class="clear-list" @click="clearTable()" variant="btn btn-secondary">
          Clear&nbsp;
          <span class="trash">
            <font-awesome-icon icon="fa-solid fa-trash" style="height: 20px"></font-awesome-icon>
          </span>
        </b-button>
        <br><br>

        <!--Table containing reports from recently classified URLs-->
        <table class="table table-hover">
          <thead>
            <tr>
              <th scope="col">URL</th>
              <th scope="col">Classified as</th>
              <th scope="col">Reliability</th>
              <th scope="col">Algorithm</th>
            </tr>
          </thead>

          <!--TODO: Vertically center detection reports-->
          <tbody v-for="detection, index in detections" :key="index">
            <tr class="each-detect">
              <td>{{ detection.URL }}</td>
              <td>{{ detection.Type }}</td>
              <td>{{ detection.Probability }}</td>
              <td>{{ detection.Algorithm }}</td>
            </tr>
          </tbody>
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
    name: "URLReports",

    data() {
      return {
        selected: 'Select an algorithm',
        detections: [],
        detectionForm: 
        {
          'URL': ''
        },
        // Regular expression to handle inputs, checking if it's a valid URL
        validateURL: new RegExp(/[-a-zA-Z0-9@:%._+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_+.~#?&//=]*)?/gi),
      };
    },

    methods: {

      // GET method: Requests all recently classified URLs information for displaying
      getDetections() {
        const path = "http://localhost:5000";
        axios
          .get(path)
          .then((res) => {
            this.detections = res.data.detections;
          })

          .catch((err) => {
            alert(err);
          });
      },

      // POST method: Sends the URL and selected algorithm for the application Back-end, which will classify the URL
      classifyURL(payload) {

        const path = 'http://localhost:5000';

        // TODO: Show possible errors loading the algorithms as dismissible pop-ups in the GUI
        axios
          .post(path, payload)
          .then((res) => {
            let status = res.data.status;
            if (String(status) === 'failed')
              alert('It occurred an error loading the algorithm!');
            this.getDetections();
          })

          .catch((err) => {
            alert(err);
            this.getDetections();
          });
      },

      // Always clears form after each request, enhancing UX (Avoids having to delete field for every new request)
      clearForm()
      {
        this.detectionForm.URL = '';
        this.selected = 'Select an algorithm';
      },

      // Input handling by the user
      checkInputs() {

        // Removes spaces from URL's edges ('  google .com ' => 'google .com')
        let newURL = String(this.detectionForm.URL).trim();
        let urlInput = document.getElementById('form-url-input');

        // If it's a valid URL, the submission process can occur, else returns an error feedback message (verbal and visual)
        if (newURL.match(this.validateURL))
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

        // Changes the form field class to display visual feedback that the input is appropriate
        let formControl = field.parentElement;
        formControl.className = 'input-form-control success';

        // Stops showing feedback after a 2,5 seconds delay
        setTimeout(function() {
          formControl.className = 'input-form-control';
        }, 2500);
      },

      setErrorFor(field, message) {

        let formControl = field.parentElement;
        let small = formControl.querySelector('b-small');

        // Changes the form field class to display verbal and visual feedback that the input is unsuitable
        formControl.className = 'input-form-control error';
        small.innerText = message;
      },

      onSubmit(e) {
        e.preventDefault();
        let check = this.checkInputs();

        if (check) {

          const payload = {
            URL: this.detectionForm.URL,
            Algorithm: this.selected
          };

          this.classifyURL(payload);
        }
        this.clearForm();
      },

      clearTable() {
        const path = 'http://localhost:5000';
        const payload = {'action': 'clear'}

        axios
          .post(path, payload)
          .then((res) => {
            let status = res.data.status;
            if (String(status) === 'failed')
              alert('The table is already empty!');
            this.getDetections();
          })

          .catch((err) => {
            alert(err);
            this.getDetections();
          });
      }
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

  select {
    padding: 10px;
  }

  table {
    border-radius: 10px;
    color: white;
    background-color: #201c1c;
    background-repeat: repeat;
    background-position: center;
  }

  #form-url-input {
    margin: 0 auto;
    border-radius: 5px;
    width: 90%;
  }

  .jumbotron {
    position: absolute;
    width: 90%;
    top: 5%;
    left: 5%;
    background-image: url("../assets/cyber.jpg");
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
    border: 2px solid #73ff00;
    margin-top: 30px;
  }

  .clear-list {
    border-radius: 5px;
    border: 2px solid #201c1c;
  }

  .each-detect:hover {
    color: aqua;
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
