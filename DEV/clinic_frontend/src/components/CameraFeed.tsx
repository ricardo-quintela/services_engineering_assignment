import { ChangeEvent, useEffect, useRef, useState } from "react";
import { Button, Container, Form } from "react-bootstrap";

const CameraFeed = () => {
    const videoRef = useRef<any>(null);
    const photoRef = useRef<any>(null);

    const [deviceFound, setDeviceFound] = useState(true);
    const [hasPhoto, setHasPhoto] = useState(false);

    const getVideo = () => {
        navigator.mediaDevices
            .getUserMedia({ video: { width: 1920, height: 1080 } })
            .then((stream) => {
                if (videoRef.current === null) return;

                let video = videoRef.current;
                video.srcObject = stream;
                video.play();
            })
            .catch(() => setDeviceFound(false));
    };

    useEffect(() => {
        getVideo();
    }, [videoRef]);

    const fileSelectedHandler = (event: ChangeEvent) => {
        console.log(event);
    }

    return (
        <Container>
            {deviceFound && (
                <>
                    <Container>
                        <video ref={videoRef} />
                        <Button>SNAP</Button>
                    </Container>
                    <Container
                        className={"result" + (hasPhoto ? "-photo" : "")}
                    >
                        <canvas ref={photoRef} />
                        <Button>Close</Button>
                    </Container>
                </>
            )}

            {!deviceFound && <>
                <Form.Label htmlFor="selectImage">Imagem</Form.Label>
                <Form.Control type="file" id="selectImage" accept="image/jpeg" onChange={fileSelectedHandler}></Form.Control>
                <Form.Text>A imagem deve ser no formato JPEG (.jpg ou .jpeg) e não deve ultrapassar os 25Kb</Form.Text>
            </>}
        </Container>
    );
};

export default CameraFeed;
