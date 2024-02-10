## 프로젝트 개요
2D 사진들을 토대로 제작된 인체의 3D STL 파일을 가공하여 **개인 맞춤 의료 기구를 제작**하는 프로그램을 제작하는 프로젝트

고려대학교 산학캡스톤디자인 수업 프로젝트

- 프로젝트 기간: `23.09` ~ `23.12`
- 담당 역할: STL 파일을 토대로 개인 맞춤 기구를 만들고, 3D 프린트 진행

## 핵심 기능
- 인체 3D STL 파일을 가공하여 개인 맞춤 보조 기구의 STL을 반환
- 이를 위해 손목 축 정렬, 스케일링 등의 가공 과정 거침

## 도전 과제 및 해결책
- `NeRF` 기술을 활용한 앱에서 제공하는 STL 파일이 스케일이 맞지 않은 문제를 손목의 가장 얇은 부분의 길이를 직접 측정함으로 스케일을 맞춤
- STL 파일에서 손목의 가장 얇은 부분은 축을 기준으로 단면의 점들까지의 거리가 가장 짦은 부분을 손목으로 인식
- ML에서 데이터의 방향성을 정렬하는 `PCA` 분석 기법을 활용하여 축 정렬

## 프로젝트 확장 가능성
- 손목에서 더 나아가 인체의 모든 부위에 대한 맞춤 기구 제작 가능
- 특정 부위의 여러 사진만 있으면 보조 기구를 제작할 수 있다는 점에서 의료 서비스가 낙후된 곳에서의 서비스 지원 가능

## 프로젝트 보고서
![프로젝트 이미지](report.png)