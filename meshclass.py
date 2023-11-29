import trimesh
from sklearn.decomposition import PCA
import numpy as np

class Mesh:
    def __init__(self, meshfile):
        self.meshfile = meshfile
        self.mesh = trimesh.load(meshfile)
        self.max_z_value = self.get_max_z_value()
        self.width = self.get_width()
        self.origin = self.get_wrist_coordinate()
        self.min_z_value = self.get_min_z_value()
    
    def update_fields(self):
        # Update all relevant fields
        self.max_z_value = self.get_max_z_value()
        self.width = self.get_width()
        self.origin = self.get_wrist_coordinate()
        self.min_z_value = self.get_min_z_value()

        return self
    
    def flip(self):
        transformation_matrix = np.array([
            [1, 0, 0, 0],
            [0, -1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ])
        self.mesh.apply_transform(transformation_matrix)
        self.update_fields()
        return self
    
    def save(self, filename=None):
        # If no filename is provided, use the original file name
        if filename is None:
            filename = self.meshfile
        self.mesh.export(filename)

        return self

    def run_pca(self):
        # Get vertices
        vertices = np.array(self.mesh.vertices)

        # Compute PCA
        pca = PCA(n_components=3)
        pca.fit_transform(vertices)

        # Align mesh model with axis
        angle_0 = np.arccos(np.clip(np.dot([0, 0, 1], pca.components_[0]), -1.0, 1.0))
        direction_0 = np.cross(pca.components_[0], [0, 0, 1])
        rotation_matrix_0 = trimesh.transformations.rotation_matrix(angle=angle_0, direction=direction_0)
        self.mesh.apply_transform(rotation_matrix_0)

        axis_1 = pca.components_[1]
        axis_1 = np.array([axis_1[0], axis_1[1], axis_1[2], 0])
        axis_1 = np.dot(rotation_matrix_0, axis_1)
        axis_1 = axis_1[:3]
        angle_1 = np.arccos(np.clip(np.dot([1, 0, 0], axis_1), -1.0, 1.0))
        direction_1 = np.cross([1, 0, 0], axis_1)
        rotation_matrix_1 = trimesh.transformations.rotation_matrix(angle=angle_1, direction=direction_1)
        self.mesh.apply_transform(rotation_matrix_1)
        
        return self

    def render(self):
        # Create a scene
        scene = self.mesh.scene()

        # Parameters for the axes
        axis_radius = 2  # Radius of the axes
        axis_length = 200  # Length of the axes

        # Red Axis (X-axis)
        x_axis_cylinder = trimesh.creation.cylinder(radius=axis_radius, height=axis_length, sections=32, 
                                                    transform=trimesh.transformations.rotation_matrix(np.pi/2, [0, 1, 0]))
        x_axis_cylinder.visual.face_colors = (255, 0, 0)
        scene.add_geometry(x_axis_cylinder)

        x_arrow_transform = trimesh.transformations.rotation_matrix(np.pi/2, [0, 1, 0])
        x_arrow_position = np.array([1, 0, 0]) * axis_length * 0.5
        x_arrow_transform[0:3, 3] = x_arrow_position
        x_arrow_cone = trimesh.creation.cone(radius=axis_radius * 2, height=axis_radius * 4, sections=32, transform=x_arrow_transform)
        x_arrow_cone.visual.face_colors = (255, 0, 0)
        scene.add_geometry(x_arrow_cone)

        # Green Axis (Y-axis)
        y_axis_cylinder = trimesh.creation.cylinder(radius=axis_radius, height=axis_length, sections=32, 
                                                    transform=trimesh.transformations.rotation_matrix(np.pi/2, [-1, 0, 0]))
        y_axis_cylinder.visual.face_colors = (0, 255, 0)
        scene.add_geometry(y_axis_cylinder)

        y_arrow_transform = trimesh.transformations.rotation_matrix(np.pi/2, [-1, 0, 0])
        y_arrow_position = np.array([0, 1, 0]) * axis_length * 0.5
        y_arrow_transform[0:3, 3] = y_arrow_position
        y_arrow_cone = trimesh.creation.cone(radius=axis_radius * 2, height=axis_radius * 4, sections=32, transform=y_arrow_transform)
        y_arrow_cone.visual.face_colors = (0, 255, 0)
        scene.add_geometry(y_arrow_cone)

        # Blue Axis (Z-axis)
        z_axis_cylinder = trimesh.creation.cylinder(radius=axis_radius, height=axis_length, sections=32)
        z_axis_cylinder.visual.face_colors = (0, 0, 255)
        scene.add_geometry(z_axis_cylinder)

        z_arrow_transform = np.eye(4)
        z_arrow_position = np.array([0, 0, 1]) * axis_length * 0.5
        z_arrow_transform[0:3, 3] = z_arrow_position
        z_arrow_cone = trimesh.creation.cone(radius=axis_radius * 2, height=axis_radius * 4, sections=32, transform=z_arrow_transform)
        z_arrow_cone.visual.face_colors = (0, 0, 255)
        scene.add_geometry(z_arrow_cone)

        # Show the scene
        scene.show()

        return self


    def get_max_z_value(self):
        # Return the maximum Z value from the mesh vertices
        return np.max(self.mesh.vertices[:, 2])

    def translate_z_direction(self, translation_amount):
        translation_matrix = trimesh.transformations.translation_matrix([0, 0, translation_amount])
        self.mesh.apply_transform(translation_matrix)
        self.update_fields()
        return self

    def scale(self, scale_factor):
        # Apply the scaling to the mesh
        self.mesh.apply_scale(scale_factor)
        self.update_fields()

        # Return self for method chaining if needed
        return self

    def get_width(self):
        vertices = self.mesh.vertices
        th = (vertices[:,1].max())*0.5+(vertices[:,1].min())*0.5
        vertices = vertices[vertices[:,1]>th]
        length = vertices[:,2].max()-vertices[:,2].min()
        var_min = 100000000

        width = 0
        for i in range(20,80):

            tmp_vertices = vertices[vertices[:,2].min()+length*(i-0.5)/100<=vertices[:,2]]
            tmp_vertices = tmp_vertices[tmp_vertices[:,2]<=vertices[:,2].min()+length*(i+0.5)/100]
            
            # Check if tmp_vertices is not empty
            if tmp_vertices.size > 0:
                tmp = (tmp_vertices[:,0].max()-tmp_vertices[:,0].min())

                tmp_vertices_ = vertices[vertices[:,2].min()+length*(i-1.5)/100<=vertices[:,2]]
                tmp_vertices_ = tmp_vertices_[tmp_vertices_[:,2]<=vertices[:,2].min()+length*(i-0.5)/100]
                
                # Check if tmp_vertices_ is not empty
                if tmp_vertices_.size > 0:
                    tmp_ = (tmp_vertices_[:,0].max()-tmp_vertices_[:,0].min())

                    if tmp < var_min and tmp*1.08 < tmp_:
                        var_min = tmp
                        width = tmp
            else:
                # Handle the case where the array is empty
                # You might want to set width to a default value or continue to the next iteration
                width = 100

        return width


    def get_wrist_coordinate(self):
        vertices = self.mesh.vertices
        th = (vertices[:,1].max())*0.5 + (vertices[:,1].min())*0.5
        vertices = vertices[vertices[:,1] > th]
        length = vertices[:,2].max() - vertices[:,2].min()
        var_min = 100000000
        var_mini = 0
        x = 0
        y = 0
        z = 0

        for i in range(20, 80):
            tmp_vertices = vertices[vertices[:,2].min() + length*(i-0.5)/100 <= vertices[:,2]]
            tmp_vertices = tmp_vertices[tmp_vertices[:,2] <= vertices[:,2].min() + length*(i+0.5)/100]

            if tmp_vertices.size > 0:
                tmp = (tmp_vertices[:,0].max() - tmp_vertices[:,0].min())

                tmp_vertices_ = vertices[vertices[:,2].min() + length*(i-1.5)/100 <= vertices[:,2]]
                tmp_vertices_ = tmp_vertices_[tmp_vertices_[:,2] <= vertices[:,2].min() + length*(i-0.5)/100]

                if tmp_vertices_.size > 0:
                    tmp_ = (tmp_vertices_[:,0].max() - tmp_vertices_[:,0].min())

                    if tmp < var_min and tmp*1.08 < tmp_:
                        var_min = tmp
                        var_mini = i
                        x = (tmp_vertices[:,0].max() + tmp_vertices[:,0].min()) / 2
                        y = tmp_vertices[:,1].max()
                        z = vertices[:,2].min() + var_mini * length / 100
            else:
                # Handle the case where tmp_vertices is empty
                continue

        return (x, y, z)

        
    
    def change_origin_to_wrist(self):
        # Use the origin from the get_wrist_coordinate method
        self.mesh.apply_translation([-self.origin[0], -self.origin[1], -self.origin[2]])
        self.update_fields()
        return self

    def print_values(self):
        print(str(self.meshfile))
        print("max z value: " + str(self.max_z_value))
        print("min z value: " + str(self.min_z_value))
        print("width value: " + str(self.width))
        print("origin value: " + str(self.origin))

    
        return self
    
    def smoothen(self):
        self.mesh = trimesh.smoothing.filter_laplacian(self.mesh)
        return self
    
    def get_min_z_value(self):
        # Compute the minimum Z value from the mesh vertices
        self.min_z_value = np.min(self.mesh.vertices[:, 2])
        return self.min_z_value
    
    def rotate_x_axis(self):
        # Define the angle of rotation in radians (90 degrees)
        angle = - np.pi / 2  # -90 degrees in radians

        # Create a rotation matrix around the X-axis
        rotation_matrix = trimesh.transformations.rotation_matrix(angle, [1, 0, 0])

        # Apply the rotation to the mesh
        self.mesh.apply_transform(rotation_matrix)

        # Update the fields to reflect the new orientation
        self.update_fields()

        # Return self for method chaining if needed
        return self
    
    def rotate_z_axis(self):

        # Define the angle of rotation in radians (90 degrees)
        angle = np.pi  # 90 degrees in radians

        # Create a rotation matrix around the X-axis
        rotation_matrix = trimesh.transformations.rotation_matrix(angle, [0, 0, 1])

        # Apply the rotation to the mesh
        self.mesh.apply_transform(rotation_matrix)

        # Update the fields to reflect the new orientation
        self.update_fields()

        # Return self for method chaining if needed
        return self

    def rotate(self, axis, degree):
        # Convert degree to radians
        angle = np.radians(degree)

        # Rotation axis based on input
        if axis.lower() == 'x':
            rotation_axis = [1, 0, 0]
        elif axis.lower() == 'y':
            rotation_axis = [0, 1, 0]
        elif axis.lower() == 'z':
            rotation_axis = [0, 0, 1]
        else:
            raise ValueError("Axis must be 'x', 'y', or 'z'")

        # Create a rotation matrix
        rotation_matrix = trimesh.transformations.rotation_matrix(angle, rotation_axis)

        # Apply the rotation to the mesh
        self.mesh.apply_transform(rotation_matrix)

        # Update fields to reflect the new orientation
        self.update_fields()

        # Return self for method chaining
        return self