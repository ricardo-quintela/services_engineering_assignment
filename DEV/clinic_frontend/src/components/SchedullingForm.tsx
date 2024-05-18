import axios from "axios";
import "bootstrap/dist/css/bootstrap.min.css";
import { Carousel } from "react-bootstrap";
import { FormEvent, useState } from "react";

import atanagildoImagem from "../img/atanagildo.jpg";
import manuelaImagem from "../img/manuela.jpg";
import semPreferenciaImagem from "../img/sem_preferencia.png";
import { NotificationData } from "../interfaces/notification";
import { getCookies, setCookie } from "../cookies";

axios.defaults.withCredentials = true;

function SchedullingForm (){
    // Mexemos na imagem e guardamos o estado atual
    const [imagemAtual, setImagemAtual] = useState(atanagildoImagem);
    const handleChangeSlide = (eventKey: number) => {
        if (eventKey === 0) {
            setImagemAtual("NADA");
        } else if (eventKey === 1){
            setImagemAtual("Homem");
        } else {
            setImagemAtual("Mulher");
        }
    };

    // Preenchemos o formulário e enviamos ao endpoint
    const handleSumbmit = (e: FormEvent) => {
        e.preventDefault();
        const payload = e.target as typeof e.target & {
            inputData: { value: string };
            inputHora: { value: string };
            inputEspecialidade: { value: string };
        };
        
        axios
            .post(process.env.REACT_APP_API_URL + "marcacao/", {
                data: payload.inputData.value,
                hora: payload.inputHora.value,
                especialidade: payload.inputEspecialidade.value,
                medico: imagemAtual,
                jwt: document.cookie.split("=")[1].trim()
            }
            ).then((response) => {
                console.log(response);
            })
            .catch((response) => console.log(response));
    };

    return (
        <>
            <h1>Marcação de consulta</h1>
            <form
                className="d-flex p-5 flex-column gap-3 border"
                onSubmit={handleSumbmit}
            >
                <div>
                    <h5>Data</h5>
                    <input
                        className="form-control"
                        type="date"
                        id="inputData"
                    />
                </div>
                <div>
                    <h5>Hora</h5>
                    <select
                        className="form-select"
                        id="inputHora"
                        defaultValue="Escolha a sua hora"
                    >
                        <option value="0"> Escolha a sua hora </option>
                        <option value="10">10H</option>
                        <option value="11">11H</option>
                        <option value="12">12H</option>
                        <option value="13">13H</option>
                        <option value="15">15H</option>
                        <option value="16">16H</option>
                        <option value="17">17H</option>
                        <option value="18">18H</option>
                        <option value="19">19H</option>
                    </select>
                </div>
                <div>
                    <h5>Especialidade</h5>
                    <select
                        className="form-select"
                        id="inputEspecialidade"
                        defaultValue="Escolha o que procura"
                    >
                        <option value="0"> Escolha o que procura </option>
                        <option value="1">Mobilidade</option>
                        <option value="2">Amputados</option>
                        <option value="3">Massagens</option>
                        <option value="3">Mais cenas e tal</option>
                    </select>
                </div>
                <div>
                    <h5> Escolha o seu médico </h5>
                    <Carousel
                        data-bs-theme="dark"
                        indicators={false}
                        pause={"hover"}
                        interval={null}
                        id="inputMedico"
                        onSelect={handleChangeSlide}
                    >
                        <Carousel.Item>
                            <div className="text-center">
                                <span> Sem preferência </span>
                                <img
                                    className="d-block mx-auto"
                                    src={semPreferenciaImagem}
                                    alt="Second slide"
                                    style={{
                                        maxHeight: "100px",
                                        maxWidth: "100px",
                                    }}
                                />
                            </div>
                        </Carousel.Item>
                        <Carousel.Item>
                            <div className="text-center">
                                <span> Atanagildo </span>
                                <img
                                    className="d-block mx-auto"
                                    src={atanagildoImagem}
                                    alt="Second slide"
                                    style={{
                                        maxHeight: "100px",
                                        maxWidth: "100px",
                                    }}
                                />
                            </div>
                        </Carousel.Item>
                        <Carousel.Item>
                            <div className="text-center">
                                <span> Manuela </span>
                                <img
                                    className="d-block mx-auto"
                                    src={manuelaImagem}
                                    alt="Second slide"
                                    style={{
                                        maxHeight: "100px",
                                        maxWidth: "100px",
                                    }}
                                />
                            </div>
                        </Carousel.Item>
                    </Carousel>
                </div>
                <button className="btn btn-primary" type="submit">
                    Submit
                </button>
            </form>
        </>
    );
}

export default SchedullingForm;
