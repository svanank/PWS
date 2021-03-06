from Master.models import Country, State, Term, Customer, Port, Unit, ContainerSize, Vessel, Item
from datetime import datetime
from django.db.models import Q
from django.utils import timezone
import requests

class pwsRepo:

    def AdvSearchState(SearchBy=''):
        States = []

        try:
            States = State.objects.filter(IsActive=True, Name__icontains=SearchBy).order_by('Name')
        except Exception as e:
            print(e)

        return States
        
    def AdvSearchCountry(SearchBy=''):
        Countries = []

        try:
            Countries = Country.objects.filter(Q(Name__icontains=SearchBy) | Q(IsoCode__icontains=SearchBy), IsActive=True).order_by('Name')
        except Exception as e:
            print(e)

        return Countries
        
    def AdvSearchTerm(SearchBy=''):
        Terms = []

        try:
            Terms = Term.objects.filter(IsActive=True, Name__icontains=SearchBy).order_by('Name')
        except Exception as e:
            print(e)

        return Terms

    def AdvSearchCustomer(SearchBy=''):
        Customers = []

        try:
            Customers = Customer.objects.filter(IsActive=True, Name__icontains=SearchBy).order_by('Name')
        except Exception as e:
            print(e)

        return Customers

    def PartialCustomerList(SearchBy=''):
        Customers = []

        try:
            Customers = Customer.objects.filter(IsActive=True, Name__icontains=SearchBy).order_by('Name')[:100]
        except Exception as e:
            print(e)

        return Customers
        
    def PartialPortList(SearchBy=''):
        Ports = []
        
        try:
            Ports = Port.objects.filter(IsActive=True, Name__icontains=SearchBy).order_by('Name')[:100]
        except Exception as e:
            print(e)

        return Ports

    def PartialUnitList(SearchBy=''):
        Units = []
        
        try:
            Units = Unit.objects.filter(Q(ShortName__icontains=SearchBy) | Q(FullName__icontains=SearchBy), IsActive=True).order_by('ShortName', 'FullName')[:100]
        except Exception as e:
            print(e)

        return Units
        
    def PartialContainerSizeList(SearchBy=''):
        ContainerSizes = []
        
        try:
            ContainerSizes = ContainerSize.objects.filter(IsActive=True, Name__icontains=SearchBy).order_by('Name')[:100]
        except Exception as e:
            print(e)
        
        return ContainerSizes

    def PartialVesselList(SearchBy=''):
        Vessels = []
        
        try:
            Vessels = Vessel.objects.filter(IsActive=True, Name__icontains=SearchBy).order_by('Name')[:100]
        except Exception as e:
            print(e)
        
        return Vessels

    def PartialItemList(SearchBy=''):
        Items = []
        
        try:
            Items = Item.objects.filter(Q(Code__icontains=SearchBy) | Q(Name__icontains=SearchBy), IsActive=True).order_by('Code','Name')[:100]
        except Exception as e:
            print(e)
        
        return Items

    def LoadCustomer(CustomerID):
        CustomerDto = Customer()

        try:
            CustomerDto = Customer.objects.get(ID=CustomerID, IsActive=True)
        except Exception as e:
            print(e)
        
        return CustomerDto
        
    def LoadPort(PortID):
        PortDto = Port()
        
        try:
            PortDto = Port.objects.get(ID=PortID, IsActive=True)
        except Exception as e:
            print(e)
        
        return PortDto

    def LoadUnit(UnitID):
        UnitDto = Unit()
        
        try:
            UnitDto = Unit.objects.get(ID=UnitID, IsActive=True)
        except Exception as e:
            print(e)
        
        return UnitDto
        
    def LoadContainerSize(ContainerSizeID):
        ContainerSizeDto = ContainerSize()
        
        try:
            ContainerSizeDto = ContainerSize.objects.get(ID=ContainerSizeID, IsActive=True)
        except Exception as e:
            print(e)
        
        return ContainerSizeDto

    def LoadVessel(VesselID):
        VesselDto = Vessel()
        
        try:
            VesselDto = Vessel.objects.get(ID=VesselID, IsActive=True)
        except Exception as e:
            print(e)
        
        return VesselDto

    def LoadItem(ItemID):
        ItemDto = Item()
        
        try:
            ItemDto = Item.objects.get(ID=ItemID, IsActive=True)
        except Exception as e:
            print(e)
        
        return ItemDto

    def UpsertCountry():
        rtn = False
        insert = 0

        try:
            Record = Country.objects.all().count()

            if Record == 0:
                res = requests.get('https://countrycode.org/api/countryCode/countryMenu')
                Countries = res.json()

                for country in Countries:
                    c = Country.objects.create(Name=country['name'], IsoCode=str(country['code']).upper(), IsActive=True, CreateDate= datetime.now(tz=timezone.utc), 
                    CreateBy=None, UpdateDate=datetime.now(tz=timezone.utc), UpdateBy=None)

                    if(c.ID):
                        insert += 1

                if (len(Countries) == insert):
                    rtn = True
                    
            else:
                rtn = True

        except Exception as e:
            rtn = False
            print(e)
            
        return rtn
    
    def UpsertCustomer(Dto):
        rtn = False
        CustomerID = None
        StateDto = None
        CountryDto = None
        TermDto = None
        UpsertDto = None
        
        try:
            StateDto = State.objects.get(ID=Dto['StateID'])
            CountryDto = Country.objects.get(ID=Dto['CountryID'])
            TermDto = Term.objects.get(ID=Dto['TermID'])
            
            if Dto['CustomerID'] == None:
                
                UpsertDto = Customer.objects.create(Name=Dto['Name'], Pic=Dto['Pic'], MobileNo=Dto['MobileNo'], TelNo=Dto['TelNo'],
                            FaxNo=Dto['FaxNo'], Email=Dto['Email'], Address=Dto['Address'], City=Dto['City'], PostCode=Dto['PostCode'],
                            State=StateDto, Country=CountryDto, Term=TermDto, LimitAmount=Dto['LimitAmount'], IsAllowInvoice=Dto['IsAllowInvoice'],
                            IsAllowDo=Dto['IsAllowDo'], IsActive=True, CreateDate=datetime.now(tz=timezone.utc), CreateBy=None,
                            UpdateDate=datetime.now(tz=timezone.utc), UpdateBy=None)
                
                if UpsertDto.ID:
                    rtn = True
                    CustomerID = UpsertDto.ID

            else:
                UpsertDto = Customer.objects.get(ID=Dto['CustomerID'])
                UpsertDto.Name = Dto['Name']
                UpsertDto.Pic = Dto['Pic']
                UpsertDto.MobileNo = Dto['MobileNo']
                UpsertDto.TelNo = Dto['TelNo']
                UpsertDto.FaxNo = Dto['FaxNo']
                UpsertDto.Email = Dto['Email']
                UpsertDto.Address = Dto['Address']
                UpsertDto.City = Dto['City']
                UpsertDto.PostCode = Dto['PostCode']
                UpsertDto.State = StateDto
                UpsertDto.Country = CountryDto
                UpsertDto.Term = TermDto
                UpsertDto.LimitAmount = Dto['LimitAmount']
                UpsertDto.IsAllowInvoice = Dto['IsAllowInvoice']
                UpsertDto.IsAllowDo = Dto['IsAllowDo']
                UpsertDto.IsActive = True
                UpsertDto.UpdateDate = datetime.now(tz=timezone.utc) 
                UpsertDto.UpdateBy = None
                UpsertDto.save()
                rtn = True
                CustomerID = Dto['CustomerID']
                        
        except Exception as e:
            print(e)
        
        return { 'rtn' : rtn, 'CustomerID' : CustomerID }
        
    def UpsertPort(Dto):
        rtn = False
        PortID = None
        CountryDto = None
        UpsertDto = None
        
        try:
            CountryDto = Country.objects.get(ID=Dto['CountryID'])
            
            if Dto['PortID'] == None:
                
                UpsertDto = Port.objects.create(Code=Dto['Code'], Name=Dto['Name'], IsSpecial=Dto['IsSpecial'],
                            Country=CountryDto, IsActive=True, CreateDate=datetime.now(tz=timezone.utc), CreateBy=None,
                            UpdateDate=datetime.now(tz=timezone.utc), UpdateBy=None)
                            
                if UpsertDto.ID:
                    rtn = True
                    PortID = UpsertDto.ID
                    
            else:
                UpsertDto = Port.objects.get(ID=Dto['PortID'])
                UpsertDto.Code = Dto['Code']
                UpsertDto.Name = Dto['Name']
                UpsertDto.IsSpecial = Dto['IsSpecial']
                UpsertDto.Country = CountryDto
                UpsertDto.IsActive = True
                UpsertDto.UpdateDate = datetime.now(tz=timezone.utc) 
                UpsertDto.UpdateBy = None
                UpsertDto.save()
                rtn = True
                PortID = Dto['PortID']
                        
        except Exception as e:
            print(e)
        
        return { 'rtn' : rtn, 'PortID' : PortID }

    def UpsertUnit(Dto):
        rtn = False
        UnitID = None
        UpsertDto = None
        
        try:
            
            if Dto['UnitID'] == None:
                
                UpsertDto = Unit.objects.create(Code=Dto['Code'], ShortName=Dto['ShortName'], FullName=Dto['FullName'],
                            IsActive=True, CreateDate=datetime.now(tz=timezone.utc), CreateBy=None,
                            UpdateDate=datetime.now(tz=timezone.utc), UpdateBy=None)
                            
                if UpsertDto.ID:
                    rtn = True
                    UnitID = UpsertDto.ID
                    
            else:
                UpsertDto = Unit.objects.get(ID=Dto['UnitID'])
                UpsertDto.Code = Dto['Code']
                UpsertDto.ShortName = Dto['ShortName']
                UpsertDto.FullName = Dto['FullName']
                UpsertDto.IsActive = True
                UpsertDto.UpdateDate = datetime.now(tz=timezone.utc) 
                UpsertDto.UpdateBy = None
                UpsertDto.save()
                rtn = True
                UnitID = Dto['UnitID']
                        
        except Exception as e:
            print(e)
        
        return { 'rtn' : rtn, 'UnitID' : UnitID }
        
    def UpsertContainerSize(Dto):
        rtn = False
        ContainerSizeID = None
        UpsertDto = None
        
        try:
            
            if Dto['ContainerSizeID'] == None:
                
                UpsertDto = ContainerSize.objects.create(Code=Dto['Code'], Name=Dto['Name'], Teus=Dto['Teus'],
                            IsActive=True, CreateDate=datetime.now(tz=timezone.utc), CreateBy=None,
                            UpdateDate=datetime.now(tz=timezone.utc), UpdateBy=None)
                            
                if UpsertDto.ID:
                    rtn = True
                    ContainerSizeID = UpsertDto.ID
                    
            else:
                UpsertDto = ContainerSize.objects.get(ID=Dto['ContainerSizeID'])
                UpsertDto.Code = Dto['Code']
                UpsertDto.Name = Dto['Name']
                UpsertDto.Teus = Dto['Teus']
                UpsertDto.IsActive = True
                UpsertDto.UpdateDate = datetime.now(tz=timezone.utc) 
                UpsertDto.UpdateBy = None
                UpsertDto.save()
                rtn = True
                ContainerSizeID = Dto['ContainerSizeID']
                        
        except Exception as e:
            print(e)
        
        return { 'rtn' : rtn, 'ContainerSizeID' : ContainerSizeID }

    def UpsertVessel(Dto):
        rtn = False
        VesselID = None
        PortOperatorDto = None
        PsaDto = None
        ShippingAgentDto = None
        UpsertDto = None
        
        try:
            PortOperatorDto = Customer.objects.get(ID=Dto['PortOperatorID'])
            PsaDto = Customer.objects.get(ID=Dto['PsaID'])
            ShippingAgentDto = Customer.objects.get(ID=Dto['ShippingAgentID'])
            
            if Dto['VesselID'] == None:
                
                UpsertDto = Vessel.objects.create(Code=Dto['Code'], Name=Dto['Name'], PortOperator=PortOperatorDto,
                            Psa=PsaDto, ShippingAgent=ShippingAgentDto, IsActive=True, CreateDate=datetime.now(tz=timezone.utc), 
                            CreateBy=None, UpdateDate=datetime.now(tz=timezone.utc), UpdateBy=None)
                            
                if UpsertDto.ID:
                    rtn = True
                    VesselID = UpsertDto.ID
                    
            else:
                UpsertDto = Vessel.objects.get(ID=Dto['VesselID'])
                UpsertDto.Code = Dto['Code']
                UpsertDto.Name = Dto['Name']
                UpsertDto.PortOperator = PortOperatorDto
                UpsertDto.Psa = PsaDto
                UpsertDto.ShippingAgent = ShippingAgentDto
                UpsertDto.IsActive = True
                UpsertDto.UpdateDate = datetime.now(tz=timezone.utc) 
                UpsertDto.UpdateBy = None
                UpsertDto.save()
                rtn = True
                VesselID = Dto['VesselID']
                        
        except Exception as e:
            print(e)
        
        return { 'rtn' : rtn, 'VesselID' : VesselID }

    def UpsertItem(Dto):
        rtn = False
        ItemID = None
        UpsertDto = None
        
        try:
            
            if Dto['ItemID'] == None:
                
                UpsertDto = Item.objects.create(Code=Dto['Code'], Name=Dto['Name'], IsActive=True, 
                            CreateDate=datetime.now(tz=timezone.utc), CreateBy=None,
                            UpdateDate=datetime.now(tz=timezone.utc), UpdateBy=None)
                            
                if UpsertDto.ID:
                    rtn = True
                    ItemID = UpsertDto.ID
                    
            else:
                UpsertDto = Item.objects.get(ID=Dto['ItemID'])
                UpsertDto.Code = Dto['Code']
                UpsertDto.Name = Dto['Name']
                UpsertDto.IsActive = True
                UpsertDto.UpdateDate = datetime.now(tz=timezone.utc) 
                UpsertDto.UpdateBy = None
                UpsertDto.save()
                rtn = True
                ItemID = Dto['ItemID']
                        
        except Exception as e:
            print(e)
        
        return { 'rtn' : rtn, 'ItemID' : ItemID }
    
    def DeleteCustomer(CustomerID):
        rtn = False

        try:
            CustomerDto = Customer.objects.get(ID=CustomerID)
            CustomerDto.IsActive = False
            CustomerDto.UpdateDate = datetime.now(tz=timezone.utc) 
            CustomerDto.UpdateBy = None
            CustomerDto.save()
            rtn = True
        except Exception as e:
            print(e)
        
        return rtn
        
    def DeletePort(PortID):
        rtn = False

        try:
            PortDto = Port.objects.get(ID=PortID)
            PortDto.IsActive = False
            PortDto.UpdateDate = datetime.now(tz=timezone.utc) 
            PortDto.UpdateBy = None
            PortDto.save()
            rtn = True
        except Exception as e:
            print(e)
        
        return rtn
        
    def DeleteUnit(UnitID):
        rtn = False

        try:
            UnitDto = Unit.objects.get(ID=UnitID)
            UnitDto.IsActive = False
            UnitDto.UpdateDate = datetime.now(tz=timezone.utc) 
            UnitDto.UpdateBy = None
            UnitDto.save()
            rtn = True
        except Exception as e:
            print(e)
        
        return rtn

    def DeleteContainerSize(ContainerSizeID):
        rtn = False

        try:
            ContainerSizeDto = ContainerSize.objects.get(ID=ContainerSizeID)
            ContainerSizeDto.IsActive = False
            ContainerSizeDto.UpdateDate = datetime.now(tz=timezone.utc) 
            ContainerSizeDto.UpdateBy = None
            ContainerSizeDto.save()
            rtn = True
        except Exception as e:
            print(e)
        
        return rtn

    def DeleteVessel(VesselID):
        rtn = False

        try:
            VesselDto = Vessel.objects.get(ID=VesselID)
            VesselDto.IsActive = False
            VesselDto.UpdateDate = datetime.now(tz=timezone.utc) 
            VesselDto.UpdateBy = None
            VesselDto.save()
            rtn = True
        except Exception as e:
            print(e)
        
        return rtn

    def DeleteItem(ItemID):
        rtn = False

        try:
            ItemDto = Item.objects.get(ID=ItemID)
            ItemDto.IsActive = False
            ItemDto.UpdateDate = datetime.now(tz=timezone.utc) 
            ItemDto.UpdateBy = None
            ItemDto.save()
            rtn = True
        except Exception as e:
            print(e)
        
        return rtn
            