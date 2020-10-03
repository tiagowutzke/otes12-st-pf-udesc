from microservices.project import Project
from microservices.test_factor import TestFactor
from microservices.project_measure import ProjectMeasure
from microservices.function_points import FunctionPoints
from microservices.feature_acceptance import FeatureAcceptance
from microservices.assertive_case_test import AssertiveCaseTest
from microservices.assertives_percentage import AssertivesPercentage
from microservices.system_general_features import SystemGerenalFeatures
from microservices.unadjusted_function_points import UnadjustedFunctionPoints
from microservices.assertives_percentage_acceptance import AssertivesPercentageAcceptance


class Broker:
    def __init__(
        self,
        request_type,
        microservice,
        payload,
        *args,
        **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.request_type = request_type
        self.microservice = microservice
        self.payload = payload

    def broker_services(self):
        if self.microservice == 'project':
            return self.project_microservice()
        elif self.microservice == 'feature_acceptance':
            return self.feature_acceptance()
        elif self.microservice == 'assertive_test_case':
            return self.assertive_case_test()
        elif self.microservice == 'assertives_percentage':
            return self.assertives_percentage()
        elif self.microservice == 'assertives_percentage_acceptance':
            return self.assertives_percentage_acceptance()
        elif self.microservice == 'function_points':
            return self.function_points()
        elif self.microservice == 'project_measure':
            return self.project_measure()
        elif self.microservice == 'system_general_features':
            return self.system_general_features()
        elif self.microservice == 'test_factor':
            return self.test_factor()
        elif self.microservice == 'unadjusted_function_points':
            return self.unadjusted_function_points()

    def project_microservice(self):
        project = Project()

        if self.request_type == 'GET':
            return project.backup()

        elif self.request_type == 'PUT':
            return project.insert(self.payload)

        elif self.request_type == 'DELETE':
            return project.delete(self.payload)

    def feature_acceptance(self):
        feature_acceptance = FeatureAcceptance()

        if self.request_type == 'GET':
            return feature_acceptance.backup()

        elif self.request_type == 'PUT':
            return feature_acceptance.insert(self.payload)

        elif self.request_type == 'DELETE':
            return feature_acceptance.delete(self.payload)

    def assertive_case_test(self):
        assertive_case_test = AssertiveCaseTest()

        if self.request_type == 'GET':
            return assertive_case_test.backup()

        elif self.request_type == 'PUT':
            return assertive_case_test.insert(self.payload)

        elif self.request_type == 'DELETE':
            return assertive_case_test.delete(self.payload)

    def assertives_percentage(self):
        assertive_percentage = AssertivesPercentage()

        if self.request_type == 'GET':
            return assertive_percentage.backup()

        elif self.request_type == 'PUT':
            return assertive_percentage.insert(self.payload)

        elif self.request_type == 'DELETE':
            return assertive_percentage.delete(self.payload)

    def assertives_percentage_acceptance(self):
        assertive_percentage_accept = AssertivesPercentageAcceptance()

        if self.request_type == 'GET':
            return assertive_percentage_accept.backup()

        elif self.request_type == 'PUT':
            return assertive_percentage_accept.insert(self.payload)

        elif self.request_type == 'DELETE':
            return assertive_percentage_accept.delete(self.payload)

    def function_points(self):
        function_points = FunctionPoints()

        if self.request_type == 'GET':
            return function_points.backup()

        elif self.request_type == 'PUT':
            return function_points.insert(self.payload)

        elif self.request_type == 'DELETE':
            return function_points.delete(self.payload)

    def project_measure(self):
        project_measure = ProjectMeasure()

        if self.request_type == 'GET':
            return project_measure.backup()

        elif self.request_type == 'PUT':
            return project_measure.insert(self.payload)

        elif self.request_type == 'DELETE':
            return project_measure.delete(self.payload)

    def system_general_features(self):
        system_general_features = SystemGerenalFeatures()

        if self.request_type == 'GET':
            return system_general_features.backup()

        elif self.request_type == 'PUT':
            return system_general_features.insert(self.payload)

        elif self.request_type == 'DELETE':
            return system_general_features.delete(self.payload)

    def test_factor(self):
        test_factor = TestFactor()

        if self.request_type == 'GET':
            return test_factor.backup()

        elif self.request_type == 'PUT':
            return test_factor.insert(self.payload)

        elif self.request_type == 'DELETE':
            return test_factor.delete(self.payload)

    def unadjusted_function_points(self):
        unadjusted_function = UnadjustedFunctionPoints()

        if self.request_type == 'GET':
            return unadjusted_function.backup()

        elif self.request_type == 'PUT':
            return unadjusted_function.insert(self.payload)

        elif self.request_type == 'DELETE':
            return unadjusted_function.delete(self.payload)





