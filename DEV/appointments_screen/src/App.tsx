// import "bootstrap/dist/css/bootstrap.min.css";
// import { useEffect, useState } from "react";
// import { Container, ListGroup } from "react-bootstrap";
// import { AppointmentData } from "./interfaces/appointment";
// import useWebSocket from "react-use-websocket";

// const App = () => {
//     const { sendMessage, lastMessage, readyState } = useWebSocket(
//         process.env.REACT_APP_WS_URI + "ws/admin/"
//     );
//     const [messageHistory, setMessageHistory] = useState<
//         MessageEvent<string>[]
//     >([]);

//     useEffect(() => {
//         if (lastMessage !== null) {
//             setMessageHistory((prev) => prev.concat(lastMessage));
//         }
//     }, [lastMessage]);

//     return (
//         <Container className="d-flex flex-column gap-5 align-items-center border p-3">
//             <h1>Consultas</h1>

//             {messageHistory.length !== 0 && (
//                 <ListGroup>
//                     {messageHistory.map((value, index) => {
//                         const appointmentData: AppointmentData = JSON.parse(
//                             value.data
//                         ).message;
//                         return (
//                             <p>
//                                 {appointmentData.hora} |{" "}
//                                 {appointmentData.cliente === undefined
//                                     ? appointmentData.user?.username
//                                     : appointmentData.cliente}{" "}
//                                 | {appointmentData.especialidade} com{" "}
//                                 {appointmentData.medico}
//                             </p>
//                         );
//                     })}
//                 </ListGroup>
//             )}
//             {messageHistory.length === 0 && (
//                 <h3 className="text-center">
//                     De momento não existem consultas
//                 </h3>
//             )}
//         </Container>
//     );
// };

// export default App;

const App = () => <></>;

export default App;
