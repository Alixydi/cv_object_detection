import cv2
from ultralytics import YOLO
import supervision as sv

def main():
    model = YOLO("yolov8m-seg.pt")
    # result = model.track(source=0, show=True)

    box_annotator = sv.BoxAnnotator(
        thickness=2,
        text_thickness=1,
        text_scale=0.5
    )

    for result in model.track(source=0, show=False, stream=True):
        
        frame = result.orig_img
        detections = sv.Detections.from_ultralytics(result)

        if result.boxes.id is not None:
            detections.tracker_id = result.boxes.id.cpu().numpy().astype(int)

        # detections = detections[(detections.class_id == 0)]

        labels = [
            f"{tracker_id} {model.model.names[class_id]} {confidence:0.2f}"
            for _, _, confidence, class_id, tracker_id
            in detections
        ]

        frame = box_annotator.annotate(scene=frame, detections=detections, labels=labels)

        cv2.imshow("yolov8", frame)

        if(cv2.waitKey(30) == 27):
            break

if __name__ == "__main__":
    main()