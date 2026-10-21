import * as THREE from 'three';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';

const el = document.getElementById('viewer');
const status = document.getElementById('viewer-status');

// Fundo transparente: a luz quente vem do gradiente do #viewer
const scene = new THREE.Scene();

const camera = new THREE.PerspectiveCamera(45, el.clientWidth / el.clientHeight, 0.1, 10000);

const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
renderer.setPixelRatio(window.devicePixelRatio);
renderer.setSize(el.clientWidth, el.clientHeight);
renderer.domElement.classList.add('absolute', 'inset-0');
el.appendChild(renderer.domElement);

scene.add(new THREE.HemisphereLight(0xfff6e8, 0x5a4a3a, 2));
const sun = new THREE.DirectionalLight(0xffe2b8, 2.2); // luz dourada, como nos renders do escritório
sun.position.set(5, 10, 5);
scene.add(sun);

const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;

new GLTFLoader().load(
  el.dataset.model,
  (gltf) => {
    const model = gltf.scene;
    scene.add(model);

    // Enquadra a câmera no tamanho do modelo
    const box = new THREE.Box3().setFromObject(model);
    const size = box.getSize(new THREE.Vector3()).length();
    const center = box.getCenter(new THREE.Vector3());
    controls.target.copy(center);
    camera.position.copy(center).add(new THREE.Vector3(size * 0.6, size * 0.4, size * 0.8));
    camera.near = size / 100;
    camera.far = size * 100;
    camera.updateProjectionMatrix();

    // Grade de piso sob o modelo, como numa prancha técnica
    const grid = new THREE.GridHelper(size * 3, 30, 0x1f3a2e, 0x1f3a2e);
    grid.position.set(center.x, box.min.y, center.z);
    grid.material.transparent = true;
    grid.material.opacity = 0.12;
    scene.add(grid);

    status.remove();
  },
  undefined,
  () => { status.textContent = 'Não foi possível carregar o modelo 3D.'; }
);

// Acompanha o tamanho do #viewer (janela, zoom do navegador, cabeçalho maior ou menor)
new ResizeObserver(() => {
  camera.aspect = el.clientWidth / el.clientHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(el.clientWidth, el.clientHeight);
}).observe(el);

renderer.setAnimationLoop(() => {
  controls.update();
  renderer.render(scene, camera);
});
