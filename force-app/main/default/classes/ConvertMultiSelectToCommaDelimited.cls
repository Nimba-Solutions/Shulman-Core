public class ConvertMultiSelectToCommaDelimited {
    @InvocableMethod(label='Convert Multi-Select to Collection of Text Values' description='Converts multi-select picklist field values to a collection of text values')
    public static List<List<String>> convertMultiSelectToCollectionOfTextValues(List<String> multiSelectValues) {
        List<List<String>> collectionOfTextValues = new List<List<String>>();
        
        for (String multiSelectValue : multiSelectValues) {
            List<String> individualValues = multiSelectValue.split(';');
            collectionOfTextValues.add(individualValues);
        }
        
        return collectionOfTextValues;
    }
}