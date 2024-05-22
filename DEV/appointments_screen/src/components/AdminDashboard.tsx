import axios from "axios";
import "bootstrap/dist/css/bootstrap.min.css";
import { useState } from "react";
import { Badge, Button } from "react-bootstrap";
import ListGroup from "react-bootstrap/ListGroup";
import { AppointmentData } from "../interfaces/appointment";

axios.defaults.withCredentials = true;

const AdminDashboard = () => {
    const [appointmentData, setAppointmentData] = useState(
        [] as AppointmentData[]
    );
    const [ranQuery, setRanQuery] = useState(false);

    if (!ranQuery) {
        axios
            .get(process.env.REACT_APP_API_URL + "appointments/")
            .then((response) => {
                setAppointmentData(response.data);
                setRanQuery(true);
            })
            .catch((err) => console.error(err));
    }

    const handleCloseAppointment = (appointmentId: number, index: number) => {
        axios
            .put(
                process.env.REACT_APP_API_URL +
                    `appointments/${appointmentId}/`,
                { estado: "closed" }
            )
            .then((response) => {
                setAppointmentData(
                    appointmentData.map((data, i) => {
                        if (i !== index) return data;
                        return response.data;
                    })
                );
            })
            .catch((err) => console.error(err));
    };

    return (
        <div className="d-flex gap-5 flex-column h-75 align-items-sm-start align-items-center">
            <h1>Lista de Consultas</h1>
            <ListGroup as="ol" numbered>
                {appointmentData.length === 0 && <p>Não existem consultas.</p>}
                {appointmentData.map((data, index) => (
                    <ListGroup.Item
                        key={data.id}
                        as="li"
                        className="d-flex flex-sm-row flex-column justify-content-between align-items-sm-center gap-3"
                    >
                        <div className="ms-2 me-auto">
                            <div className="fw-bold d-flex gap-2">
                                {data.user.username}
                                {data.estado !== "closed" && (
                                    <Badge bg="primary" pill>
                                        {
                                            {
                                                open: "Aberta",
                                                ongoing: "A decorrer",
                                                payed: "Paga",
                                            }[data.estado]
                                        }
                                    </Badge>
                                )}
                            </div>
                            {data.data_appointment} - {data.hora} -{" "}
                            {data.medico}
                        </div>

                        <Button
                            disabled={data.estado === "closed"}
                            onClick={() =>
                                handleCloseAppointment(data.id, index)
                            }
                        >
                            Fechar
                        </Button>
                    </ListGroup.Item>
                ))}
            </ListGroup>
        </div>
    );
};

export default AdminDashboard;
