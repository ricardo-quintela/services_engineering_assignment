import axios from "axios";
import "bootstrap/dist/css/bootstrap.min.css";
import { FormEvent } from "react";
import { Button } from "react-bootstrap";
import Card from "react-bootstrap/Card";
import { NotificationData } from "../interfaces/notification";

axios.defaults.withCredentials = true;

const AdminDashboard = ({
	addNotification,
}: {
	addNotification: (notificationData: NotificationData) => void;
}) => {

	return (
		<Card style={{ width: "18rem" }}>
			<Card.Body>
				<Card.Title>Facial Recognition</Card.Title>
				<Card.Text>
                    Verify a client's appointment with facial recognition software.
				</Card.Text>
				<Button variant="primary">Go</Button>
			</Card.Body>
		</Card>
	);
};

export default AdminDashboard;
