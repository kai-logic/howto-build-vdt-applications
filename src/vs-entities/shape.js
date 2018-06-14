export default class Shape {
  static getShapeTag(shapes, shapeTag) {
    for (let i = 0; i < shapes.length; i += 1) {
      for (let j = 0; j < shapes[i].tag.length; j += 1) {
        if (shapes[i].tag[j] === shapeTag) {
          return shapes[i];
        }
      }
    }
    return {};
  }

  static getShapeData(rawShape) {
    const shape = {};
    shape.id = rawShape.id;
    const rawContainerComponent = rawShape.containerComponent;

    for (let i = 0; i < rawShape.containerComponent.file.length; i += 1) {
      for (let j = 0; j < rawShape.containerComponent.file[i].uri.length; j += 1) {
        const uriPath = rawShape.containerComponent.file[i].uri[j].split('/APInoauth')[1];
        rawContainerComponent.file[i].uri[j] = `/apinoauth${uriPath}`;
      }
    }

    shape.containerComponent = rawContainerComponent;
    shape.audioComponent = rawShape.audioComponent;
    shape.videoComponent = rawShape.videoComponent;
    // Array destructuring
    [shape.tag] = rawShape.tag;
    return shape;
  }

  static getAllShapes(shapes = []) {
    const map = shapes.map(shape => Shape.getShapeData(shape));
    return map;
  }
}
