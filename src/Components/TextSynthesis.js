import React, { useState } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import './TextSynthesis.css';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faUpload, faTrashAlt } from '@fortawesome/free-solid-svg-icons';
import axios from 'axios';
import Swal from 'sweetalert2';

const TextSynthesis = () => {
  const [inputValue, setInputValue] = useState('');
  const [synthesisType, setSynthesisType] = useState('text');
  const [synthesizedResult, setSynthesizedResult] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState('');

  const handleInputChange = (event) => {
    setInputValue(event.target.value);
  };

  const handleToggleMode = () => {
    setInputValue('');
    setSynthesisType((prevType) => (prevType === 'text' ? 'file' : 'text'));
  };

  const handleSubmit = async () => {
    if (!inputValue) {
      Swal.fire({
        icon: 'error',
        title: 'Erreur',
        text: `Veuillez saisir du ${
          synthesisType === 'text' ? 'texte' : 'lien du fichier'
        } avant de cliquer sur Synthétiser.`,
      });
      return;
    }

    try {
      setIsLoading(true);
      setErrorMessage('');

      const loadingAlert = Swal.fire({
        title: 'Veuillez patienter...',
        allowOutsideClick: false,
        onBeforeOpen: () => {
          Swal.showLoading();
        },
      });

      let response;
      if (synthesisType === 'text') {
        response = await axios.post('http://localhost:5000/summarize', {
          text: inputValue, // Utilisez "filePath" ici
        });
      } else {
        response = await axios.post('http://localhost:8000/summarize', {
          filePath: inputValue, // Utilisez "filePath" ici aussi
        });
      }
      setSynthesizedResult(response.data.summary);
      loadingAlert.close();
    } catch (error) {
      console.error(error);
      setErrorMessage('An error occurred during summarization.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="container mt-5">
      <h1 className="interface-title">Résumez en <span className="span">1</span> clic</h1>
      <div className="row">
        <div className="col-md-6">
          <div className="btn-group mb-3" role="group">
            <button
              className={`btn ${synthesisType === 'text' ? 'btn-primary' : 'btn-secondary'}`}
              onClick={() => {
                setSynthesisType('text');
                setInputValue('');
              }}
            >
              Texte
            </button>
            <button
              className={`btn ${synthesisType === 'file' ? 'btn-primary' : 'btn-secondary'} ms-2`}
              onClick={() => {
                setSynthesisType('file');
                setInputValue('');
              }}
            >
              Lien Fichier
            </button>
            <button
              className="btn btn-danger ms-2"
              onClick={() => {
                setInputValue('');
                setSynthesisType('text');
              }}
            >
              <FontAwesomeIcon icon={faTrashAlt} />
            </button>
          </div>
          <div className="form-group">
            <h3>
             <label  htmlFor="textArea">
               
              </label>
            </h3>
            <textarea
              id="textArea"
              placeholder={synthesisType === 'text' ? 'copiez-collez ici votre texte' : "copiez-collez ici l'URL de votre fichier"}
              
              className={`form-control text-input`}
              value={inputValue}
              onChange={handleInputChange}
              rows={10}
            />
          </div>
          <div className="d-flex justify-content-center mt-3">
            <button
              className="btn btn-primary me-2"
              onClick={handleSubmit}
              disabled={isLoading}
            >
              {isLoading ? 'En cours...' : 'cliquez ici'}
            </button>
          </div>
          {errorMessage && <p className="text-danger mt-2">{errorMessage}</p>}
        </div>
        <div className="col-md-6">
          <div className="mt-4">
            <br />
            <h3>Résultat:</h3>
            <textarea
              className={`form-control result-textarea`}
              value={synthesizedResult}
              readOnly
              rows={10}
            />
          </div>
        </div>
      </div>
      <br /><br /><br />
      <footer className="mt-4 text-center">
        <p>Copyright © 2023 Technix</p>
      </footer>
    </div>
  );
};

export default TextSynthesis;
